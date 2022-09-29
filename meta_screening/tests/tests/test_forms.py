from copy import deepcopy
from random import choices

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_constants.constants import FEMALE, MALE, NO, NOT_APPLICABLE, POS, YES
from edc_utils.date import get_utcnow

from meta_screening.forms import (
    ScreeningPartOneForm,
    ScreeningPartThreeForm,
    ScreeningPartTwoForm,
)
from meta_screening.models.proxy_models import (
    ScreeningPartOne,
    ScreeningPartThree,
    ScreeningPartTwo,
)

from ..options import (
    get_part_one_eligible_options,
    get_part_three_eligible_options,
    get_part_two_eligible_options,
    now,
)


class ScreeningTestMixin:
    def complete_part_one(self, hospital_identifier=None, **options):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        hospital_identifier = hospital_identifier or "".join(
            [str(x) for x in choices(range(10), k=9)]  # nosec B311
        )
        data = {k: v for k, v in part_one_eligible_options.items()}
        data.update(hospital_identifier=hospital_identifier)
        data.update(**options or {})
        part_one_form = ScreeningPartOneForm(data=data)
        part_one_form.is_valid()
        self.assertEqual(part_one_form._errors, {})
        part_one_form.save()
        screening_identifier = part_one_form.instance.screening_identifier
        return ScreeningPartOne.objects.get(screening_identifier=screening_identifier)

    def complete_part_two(self, instance=None, **options):
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        data = {k: v for k, v in part_two_eligible_options.items()}
        data.update(**options or {})
        part_two_form = ScreeningPartTwoForm(data=data, instance=instance)
        part_two_form.is_valid()
        self.assertEqual(part_two_form._errors, {})
        part_two_form.save()
        screening_identifier = part_two_form.instance.screening_identifier
        return part_two_form, ScreeningPartTwo.objects.get(
            screening_identifier=screening_identifier
        )

    def complete_part_three(self, instance=None, **options):
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        data = {k: v for k, v in part_three_eligible_options.items()}
        data.update(**options or {})
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertEqual(part_three_form._errors, {})
        part_three_form.save()
        screening_identifier = part_three_form.instance.screening_identifier
        return part_three_form, ScreeningPartThree.objects.get(
            screening_identifier=screening_identifier
        )


class TestForms(ScreeningTestMixin, TestCase):
    def setUp(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        self.screening_part_one = ScreeningPartOne(**part_one_eligible_options)
        self.screening_part_one.save()

        self.screening_identifier = self.screening_part_one.screening_identifier

        self.screening_part_two = ScreeningPartTwo.objects.get(
            screening_identifier=self.screening_identifier
        )
        for k, v in part_two_eligible_options.items():
            setattr(self.screening_part_two, k, v)
        self.screening_part_two.report_datetime = now
        self.screening_part_two.save()
        # part_three_eligible_options = deepcopy(
        #     get_part_three_eligible_options(report_datetime=obj.report_datetime)
        # )
        # self.data = part_three_eligible_options

    def test_screening_form_one_ok(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        data = {k: v for k, v in part_one_eligible_options.items()}
        data.update(hospital_identifier="12345678")
        form = ScreeningPartOneForm(data=data)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_screening_form_two_ok(self):
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        form = ScreeningPartTwoForm(
            data=part_two_eligible_options, instance=self.screening_part_two
        )
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_screening_form_three_ok(self):
        obj = ScreeningPartThree.objects.get(screening_identifier=self.screening_identifier)
        obj.part_two_report_datetime = now
        obj.save()
        part_three_eligible_options = deepcopy(
            get_part_three_eligible_options(report_datetime=obj.report_datetime)
        )
        form = ScreeningPartThreeForm(data=part_three_eligible_options, instance=obj)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_screening_ok(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        data = {k: v for k, v in part_one_eligible_options.items()}
        data.update(hospital_identifier="12345111")
        form = ScreeningPartOneForm(data=data)
        form.is_valid()
        self.assertEqual(form._errors, {})
        form.save()

        screening_identifier = form.instance.screening_identifier

        instance = ScreeningPartTwo.objects.get(screening_identifier=screening_identifier)
        data = {k: v for k, v in part_two_eligible_options.items()}
        form = ScreeningPartTwoForm(data=part_two_eligible_options, instance=instance)
        form.is_valid()
        self.assertEqual(form._errors, {})
        form.save()

        instance = ScreeningPartThree.objects.get(
            screening_identifier=form.instance.screening_identifier
        )

        form = ScreeningPartThreeForm(data=part_three_eligible_options, instance=instance)
        form.is_valid()
        self.assertEqual(form._errors, {})
        form.save()

    def test_screening_two_urine_bhcg_pregnant_yes(self):
        instance = self.complete_part_one(gender=FEMALE, pregnant=YES)
        _, instance = self.complete_part_two(instance=instance)

        # if pregnant == YES, urine_bhcg_performed is applicable
        data = dict(
            part_three_report_datetime=instance.part_two_report_datetime
            + relativedelta(days=1),
            urine_bhcg_value=NOT_APPLICABLE,
            urine_bhcg_performed=NOT_APPLICABLE,
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn("urine_bhcg_performed", part_three_form._errors)
        self.assertIn(
            "This field is applicable",
            part_three_form._errors.get("urine_bhcg_performed")[0],
        )

        # if pregnant == YES and urine_bhcg_performed=NO, urine_bhcg_value is NA
        data = dict(
            part_three_report_datetime=instance.part_two_report_datetime
            + relativedelta(days=1),
            urine_bhcg_value=POS,  # WRONG
            urine_bhcg_performed=NO,
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn("urine_bhcg_value", part_three_form._errors)
        self.assertIn(
            "This field is not applicable",
            part_three_form._errors.get("urine_bhcg_value")[0],
        )

        # if pregnant == YES and urine_bhcg_performed=NO, urine_bhcg_value is NA OK
        data = dict(
            part_three_report_datetime=instance.part_two_report_datetime
            + relativedelta(days=1),
            urine_bhcg_performed=NO,
            urine_bhcg_value=NOT_APPLICABLE,
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertNotIn("urine_bhcg", part_three_form._errors)

        # if pregnant == YES and urine_bhcg_performed=YES,
        # urine_urine_bhcg_date is required
        data = dict(
            urine_bhcg_performed=YES,
            urine_bhcg_value=POS,
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn(
            "This field is required",
            part_three_form._errors.get("urine_bhcg_date")[0],
        )

        # if pregnant == YES and urine_bhcg_performed=YES and urine_bhcg is NEG
        # and urine_bhcg_date is now => OK
        data = dict(
            part_three_report_datetime=instance.part_two_report_datetime
            + relativedelta(days=1),
            urine_bhcg_value=POS,
            urine_bhcg_performed=YES,
            urine_bhcg_date=get_utcnow().date(),
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertNotIn("urine_bhcg", part_three_form._errors)

    def test_screening_two_urine_bhcg_pregnant_na(self):
        instance = self.complete_part_one(gender=FEMALE, pregnant=NOT_APPLICABLE)
        _, instance = self.complete_part_two(instance=instance)

        # if pregnant == NOT_APPLICABLE, urine_bhcg_performed is not applicable
        data = dict(
            urine_bhcg_performed=YES,
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn("urine_bhcg_performed", part_three_form._errors)
        self.assertIn(
            "This field is not applicable",
            part_three_form._errors.get("urine_bhcg_performed")[0],
        )

        # if pregnant == NOT_APPLICABLE, urine_bhcg_performed is not applicable
        data = dict(
            urine_bhcg_performed=NOT_APPLICABLE,
            urine_bhcg_value=NOT_APPLICABLE,
            urine_bhcg_date=get_utcnow().date(),
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn("urine_bhcg_date", part_three_form._errors)
        self.assertIn(
            "This field is not required",
            part_three_form._errors.get("urine_bhcg_date")[0],
        )

    def test_screening_two_urine_bhcg_pregnant_no(self):
        instance = self.complete_part_one(gender=FEMALE, pregnant=NO)
        _, instance = self.complete_part_two(instance=instance)
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        data = {k: v for k, v in part_three_eligible_options.items()}
        # gender F, pregnant=NO, urine_bhcg_performed should be yes/no
        data.update(
            dict(
                instance=instance,
                urine_bhcg_performed=NOT_APPLICABLE,
            )
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn("urine_bhcg_performed", part_three_form._errors)
        self.assertIn(
            "This field is applicable",
            part_three_form._errors.get("urine_bhcg_performed")[0],
        )
        # if pregnant == NO, urine_bhcg_performed=NO, urine_bhcg is not
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        data = {k: v for k, v in part_three_eligible_options.items()}
        data.update(
            dict(
                instance=instance,
                urine_bhcg_value=POS,
                urine_bhcg_performed=NO,
            )
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn("urine_bhcg_value", part_three_form._errors)
        self.assertIn(
            "This field is not applicable",
            part_three_form._errors.get("urine_bhcg_value")[0],
        )

        # if pregnant == NO, urine_bhcg_performed=YES, urine_bhcg_value is
        # not applicable
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        data = {k: v for k, v in part_three_eligible_options.items()}
        data.update(
            dict(
                instance=instance,
                urine_bhcg_value=NOT_APPLICABLE,
                urine_bhcg_performed=YES,
            )
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn("urine_bhcg_value", part_three_form._errors)
        self.assertIn(
            "This field is applicable",
            part_three_form._errors.get("urine_bhcg_value")[0],
        )

        # if pregnant == NO, urine_bhcg_performed=NO, urine_bhcg_value is not
        # provided
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        data = {k: v for k, v in part_three_eligible_options.items()}
        data.update(
            dict(
                instance=instance,
                pregnant=NO,
                urine_bhcg_value=None,
                urine_bhcg_performed=NO,
            )
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn("urine_bhcg_value", part_three_form._errors)
        self.assertIn(
            "This field is required.",
            part_three_form._errors.get("urine_bhcg_value")[0],
        )

        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        data = {k: v for k, v in part_three_eligible_options.items()}
        data.update(
            dict(
                instance=instance,
                urine_bhcg_date=get_utcnow().date(),
                urine_bhcg_performed=NO,
            )
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn("urine_bhcg_date", part_three_form._errors)
        self.assertIn(
            "This field is not required",
            part_three_form._errors.get("urine_bhcg_date")[0],
        )

        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        data = {k: v for k, v in part_three_eligible_options.items()}
        data.update(
            dict(
                instance=instance,
                urine_bhcg_value=POS,
                urine_bhcg_date=get_utcnow().date(),
                urine_bhcg_performed=YES,
            )
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()

    def test_screening_two_urine_bhcg_male_pregnant(self):
        instance = self.complete_part_one(gender=MALE, pregnant=NOT_APPLICABLE)
        _, instance = self.complete_part_two(instance=instance)

        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        data = {k: v for k, v in part_three_eligible_options.items()}
        data.update(dict(instance=instance, urine_bhcg_performed=YES))
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn("urine_bhcg_performed", part_three_form._errors)
        self.assertIn(
            "This field is not applicable",
            part_three_form._errors.get("urine_bhcg_performed")[0],
        )

        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        data = {k: v for k, v in part_three_eligible_options.items()}
        data.update(dict(instance=instance, urine_bhcg_performed=NO))
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertIn("urine_bhcg_performed", part_three_form._errors)
        self.assertIn(
            "This field is not applicable",
            part_three_form._errors.get("urine_bhcg_performed")[0],
        )

        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        data = {k: v for k, v in part_three_eligible_options.items()}
        data.update(
            dict(
                instance=instance,
                urine_bhcg_performed=NOT_APPLICABLE,
                urine_bhcg_value=NOT_APPLICABLE,
            )
        )
        part_three_form = ScreeningPartThreeForm(data=data, instance=instance)
        part_three_form.is_valid()
        self.assertNotIn("urine_bhcg", part_three_form._errors)

    def test_screening_creatinine(self):
        instance = self.complete_part_one(hospital_identifier="9678281237")
        _, instance = self.complete_part_two(instance=instance)
        self.complete_part_three(instance=instance, verbose=True, creatinine=9000.0)
