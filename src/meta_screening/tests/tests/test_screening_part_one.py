from copy import deepcopy

from django.db.utils import IntegrityError
from django.test import TestCase
from edc_constants.constants import FEMALE, NO, TBD, YES

from meta_edc.meta_version import PHASE_THREE, get_meta_version
from meta_screening.eligibility import EligibilityPartOne
from meta_screening.models import ScreeningPartOne

from ..options import get_part_one_eligible_options


class TestSubjectScreeningPartOneModel(TestCase):
    def test_eligibility_cls_eligible_yes(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        model_obj = ScreeningPartOne(**part_one_eligible_options)
        eligibility = EligibilityPartOne(model_obj=model_obj)
        # cls attrs
        self.assertEqual(eligibility.eligible, YES)
        self.assertDictEqual(eligibility.reasons_ineligible, {})
        # model attrs
        self.assertIsNone(getattr(model_obj, EligibilityPartOne.reasons_ineligible_fld_name))
        self.assertEqual(
            getattr(model_obj, EligibilityPartOne.eligible_fld_name),
            EligibilityPartOne.is_eligible_value,
        )

    def test_eligibility_cls_missing_eligible_tbd(self):
        """Assert missing data does not assess, eligible==TBD"""

        # try as cleaned data
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_one_eligible_options.update(gender=None)
        eligibility = EligibilityPartOne(cleaned_data=part_one_eligible_options)
        self.assertEqual(eligibility.eligible, EligibilityPartOne.eligible_value_default)
        self.assertIn("gender", eligibility.reasons_ineligible)

        # try as model
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_one_eligible_options.update(gender=None)
        model_obj = ScreeningPartOne(**part_one_eligible_options)
        eligibility = EligibilityPartOne(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, TBD)
        self.assertIsNotNone(eligibility.reasons_ineligible)
        # model attrs
        self.assertIsNotNone(
            getattr(model_obj, EligibilityPartOne.reasons_ineligible_fld_name)
        )
        self.assertEqual(
            getattr(model_obj, EligibilityPartOne.eligible_fld_name),
            EligibilityPartOne.eligible_value_default,
        )

    def test_eligibility_cls_eligible_no(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_one_eligible_options.update(gender=FEMALE, pregnant=YES)
        model_obj = ScreeningPartOne(**part_one_eligible_options)
        eligibility = EligibilityPartOne(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, NO)
        self.assertIn("pregnant", eligibility.reasons_ineligible)

    def test_defaults(self):
        opts = deepcopy(get_part_one_eligible_options())
        obj = ScreeningPartOne(**opts)
        obj.save()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertIsNone(obj.reasons_ineligible_part_one)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)
        self.assertIsNotNone(obj.screening_identifier)

    def test_hospital_id_integrity(self):
        hospital_identifier = "111"
        obj = ScreeningPartOne(age_in_years=25, hospital_identifier=hospital_identifier)
        obj.save()
        obj = ScreeningPartOne(age_in_years=25, hospital_identifier=hospital_identifier)
        try:
            obj.save()
        except IntegrityError:
            pass
        else:
            self.fail("IntegrityError unexpectedly not raised.")

    def test_eligible(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        obj = ScreeningPartOne(**part_one_eligible_options)
        EligibilityPartOne(model_obj=obj)
        obj.save()
        self.assertIsNone(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_one, YES)

    def test_ineligible(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        if get_meta_version() == PHASE_THREE:
            staying_nearby = "staying_nearby_12"
        else:
            staying_nearby = "staying_nearby_6"
        part_one_eligible_options.update({staying_nearby: NO})
        obj = ScreeningPartOne(**part_one_eligible_options)
        self.assertIsNone(obj.reasons_ineligible_part_one)
        obj.save()
        self.assertIn("Unable/Unwilling to stay nearby for", obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_one, NO)
        setattr(obj, staying_nearby, YES)
        obj.save()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertIsNone(obj.reasons_ineligible_part_one)
