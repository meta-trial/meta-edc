from django.test import TestCase, tag
from edc_constants.constants import FEMALE, MALE, YES, NOT_APPLICABLE, NO, POS, NEG
from edc_utils.date import get_utcnow
from random import choices

from ..forms import ScreeningPartOneForm, ScreeningPartThreeForm, ScreeningPartTwoForm
from ..models.proxy_models import ScreeningPartOne, ScreeningPartTwo, ScreeningPartThree
from .options import (
    part_one_eligible_options,
    part_two_eligible_options,
    part_three_eligible_options,
)


class ScreeningTestMixin:
    def setUp(self):
        self.part_one_form = None
        self.part_two_form = None
        self.part_three_form = None
        super().setUp()

    def complete_part_one(self, hospital_identifier=None, **options):
        hospital_identifier = hospital_identifier or "".join(
            [str(x) for x in choices(range(10), k=9)]
        )
        data = {k: v for k, v in part_one_eligible_options.items()}
        data.update(hospital_identifier=hospital_identifier)
        data.update(**options or {})
        self.part_one_form = ScreeningPartOneForm(data=data)
        self.part_one_form.is_valid()
        self.assertEqual(self.part_one_form._errors, {})
        self.part_one_form.save()
        screening_identifier = self.part_one_form.instance.screening_identifier
        return ScreeningPartOne.objects.get(screening_identifier=screening_identifier)

    def complete_part_two(self, instance=None, **options):
        data = {k: v for k, v in part_two_eligible_options.items()}
        data.update(**options or {})
        self.part_two_form = ScreeningPartTwoForm(data=data, instance=instance)
        self.part_two_form.is_valid()
        self.assertEqual(self.part_two_form._errors, {})
        self.part_two_form.save()
        screening_identifier = self.part_two_form.instance.screening_identifier
        return ScreeningPartTwo.objects.get(screening_identifier=screening_identifier)

    def complete_part_three(self, instance=None, **options):
        data = {k: v for k, v in part_three_eligible_options.items()}
        data.update(**options or {})
        self.part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        self.part_three_form.is_valid()
        self.assertEqual(self.part_three_form._errors, {})
        self.part_three_form.save()
        screening_identifier = self.part_three_form.instance.screening_identifier
        return ScreeningPartThree.objects.get(screening_identifier=screening_identifier)


class TestForms(ScreeningTestMixin, TestCase):
    def setUp(self):

        obj = ScreeningPartOne(**part_one_eligible_options)
        obj.save()

        self.screening_identifier = obj.screening_identifier

        obj = ScreeningPartTwo.objects.get(
            screening_identifier=self.screening_identifier
        )
        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        self.data = part_three_eligible_options

    def test_screening_form_one_ok(self):
        data = {k: v for k, v in part_one_eligible_options.items()}
        data.update(hospital_identifier="12345678")
        form = ScreeningPartOneForm(data=data)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_screening_form_two_ok(self):
        form = ScreeningPartTwoForm(data=part_two_eligible_options)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_screening_form_three_ok(self):
        form = ScreeningPartThreeForm(data=part_three_eligible_options)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_screening_ok(self):

        data = {k: v for k, v in part_one_eligible_options.items()}
        data.update(hospital_identifier="12345111")
        form = ScreeningPartOneForm(data=data)
        form.is_valid()
        self.assertEqual(form._errors, {})
        form.save()

        screening_identifier = form.instance.screening_identifier

        instance = ScreeningPartTwo.objects.get(
            screening_identifier=screening_identifier
        )
        data = {k: v for k, v in part_two_eligible_options.items()}
        form = ScreeningPartTwoForm(data=part_two_eligible_options, instance=instance)
        form.is_valid()
        self.assertEqual(form._errors, {})
        form.save()

        instance = ScreeningPartThree.objects.get(
            screening_identifier=form.instance.screening_identifier
        )

        form = ScreeningPartThreeForm(
            data=part_three_eligible_options, instance=instance
        )
        form.is_valid()
        self.assertEqual(form._errors, {})
        form.save()

    def test_screening_two_urine_bhcg_pregnant_yes(self):
        instance = self.complete_part_one(gender=FEMALE, pregnant=YES)
        instance = self.complete_part_two(instance=instance)

        # if pregnant == YES, urine_bhcg_performed is applicable
        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg=NOT_APPLICABLE,
            urine_bhcg_performed=NOT_APPLICABLE,
        )
        self.assertIn("urine_bhcg_performed", self.part_three_form._errors)
        self.assertIn(
            "This field is applicable",
            self.part_three_form._errors.get("urine_bhcg_performed")[0],
        )

        # if pregnant == YES and urine_bhcg_performed=NO, urine_bhcg is NA
        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg=POS,  # WRONG
            urine_bhcg_performed=NO,
        )
        self.assertIn("urine_bhcg", self.part_three_form._errors)
        self.assertIn(
            "This field is not applicable",
            self.part_three_form._errors.get("urine_bhcg")[0],
        )

        # if pregnant == YES and urine_bhcg_performed=NO, urine_bhcg is NA OK

        try:
            self.complete_part_three(
                instance=instance, urine_bhcg=NOT_APPLICABLE, urine_bhcg_performed=NO
            )
        except AssertionError:
            self.fail("AssertionError unexpectedly raised.")

        # if pregnant == YES and urine_bhcg_performed=YES,
        # urine_urine_bhcg_date is required
        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg=POS,
            urine_bhcg_performed=YES,
        )
        self.assertIn(
            "This field is required",
            self.part_three_form._errors.get("urine_bhcg_date")[0],
        )

        # if pregnant == YES and urine_bhcg_performed=YES and urine_bhcg is NEG
        # and urine_bhcg_date is now => OK
        try:
            self.complete_part_three(
                instance=instance,
                urine_bhcg=POS,
                urine_bhcg_performed=YES,
                urine_bhcg_date=get_utcnow().date(),
            )
        except AssertionError:
            self.fail("AssertionError unexpectedly raised.")

    def test_screening_two_urine_bhcg_pregnant_na(self):
        instance = self.complete_part_one(gender=FEMALE, pregnant=NOT_APPLICABLE)
        instance = self.complete_part_two(instance=instance)

        # if pregnant == NOT_APPLICABLE, urine_bhcg_performed is not applicable
        try:
            ScreeningPartThreeForm(
                data=dict(
                    urine_bhcg=NOT_APPLICABLE, urine_bhcg_performed=NOT_APPLICABLE
                ),
                instance=instance,
            )
        except AssertionError:
            self.fail("AssertionError unexpectedly raised.")

        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg=NOT_APPLICABLE,
            urine_bhcg_performed=YES,
        )
        self.assertIn("urine_bhcg_performed", self.part_three_form._errors)
        self.assertIn(
            "This field is not applicable",
            self.part_three_form._errors.get("urine_bhcg_performed")[0],
        )

        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg_date=get_utcnow().date(),
            urine_bhcg_performed=NOT_APPLICABLE,
        )
        self.assertIn("urine_bhcg_date", self.part_three_form._errors)
        self.assertIn(
            "This field is not required",
            self.part_three_form._errors.get("urine_bhcg_date")[0],
        )

    def test_screening_two_urine_bhcg_pregnant_no(self):
        instance = self.complete_part_one(gender=FEMALE, pregnant=NO)
        instance = self.complete_part_two(instance=instance)

        # if pregnant == NO, urine_bhcg_performed is applicable
        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg=NOT_APPLICABLE,
            urine_bhcg_performed=NOT_APPLICABLE,
        )
        self.assertIn("urine_bhcg_performed", self.part_three_form._errors)
        self.assertIn(
            "This field is applicable",
            self.part_three_form._errors.get("urine_bhcg_performed")[0],
        )

        # if pregnant == NO, urine_bhcg_performed=NO, urine_bhcg is not
        # applicable
        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg=POS,
            urine_bhcg_performed=NO,
        )
        self.assertIn("urine_bhcg", self.part_three_form._errors)
        self.assertIn(
            "This field is not applicable",
            self.part_three_form._errors.get("urine_bhcg")[0],
        )

        # if pregnant == NO, urine_bhcg_performed=YES, urine_bhcg is
        # applicable
        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg=NOT_APPLICABLE,
            urine_bhcg_performed=YES,
        )
        self.assertIn("urine_bhcg", self.part_three_form._errors)
        self.assertIn(
            "This field is applicable",
            self.part_three_form._errors.get("urine_bhcg")[0],
        )

        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg_date=get_utcnow().date(),
            urine_bhcg_performed=NO,
        )
        self.assertIn("urine_bhcg_date", self.part_three_form._errors)
        self.assertIn(
            "This field is not required",
            self.part_three_form._errors.get("urine_bhcg_date")[0],
        )

        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg=POS,
            urine_bhcg_date=get_utcnow().date(),
            urine_bhcg_performed=YES,
        )
        self.assertIn("urine_bhcg", self.part_three_form._errors)
        self.assertIn(
            "Invalid, part one says subject is not pregnant",
            self.part_three_form._errors.get("urine_bhcg")[0],
        )

        try:
            self.complete_part_three(
                instance=instance,
                urine_bhcg=NEG,
                urine_bhcg_performed=YES,
                urine_bhcg_date=get_utcnow().date(),
            )
        except AssertionError:
            self.fail("AssertionError unexpectedly raised.")

    def test_screening_two_urine_bhcg_male_pregnant(self):
        instance = self.complete_part_one(gender=MALE, pregnant=NOT_APPLICABLE)
        instance = self.complete_part_two(instance=instance)

        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg_performed=YES,
        )
        self.assertIn("urine_bhcg_performed", self.part_three_form._errors)
        self.assertIn(
            "This field is not applicable",
            self.part_three_form._errors.get("urine_bhcg_performed")[0],
        )

        self.assertRaises(
            AssertionError,
            self.complete_part_three,
            instance=instance,
            urine_bhcg_performed=NO,
        )
        self.assertIn("urine_bhcg_performed", self.part_three_form._errors)
        self.assertIn(
            "This field is not applicable",
            self.part_three_form._errors.get("urine_bhcg_performed")[0],
        )

        try:
            self.complete_part_three(
                instance=instance,
                urine_bhcg=NOT_APPLICABLE,
                urine_bhcg_performed=NOT_APPLICABLE,
            )
        except AssertionError:
            self.fail("AssertionError unexpectedly raised.")

    def test_screening_creatinine(self):
        instance = self.complete_part_one(hospital_identifier="9678281237")
        instance = self.complete_part_two(instance=instance)
        self.complete_part_three(instance=instance, verbose=True, creatinine=9000.0)
