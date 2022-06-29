from copy import deepcopy

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_constants.constants import NO, NOT_APPLICABLE, TBD, YES
from edc_utils.date import get_utcnow

from meta_pharmacy.constants import METFORMIN
from meta_screening.models import ScreeningPartOne, ScreeningPartTwo

from ...eligibility import EligibilityPartOne
from ..options import get_part_one_eligible_options, get_part_two_eligible_options


class TestScreeningPartTwo(TestCase):
    def setUp(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        model_obj = ScreeningPartOne(**part_one_eligible_options)
        model_obj.save()
        self.assertIsNone(getattr(model_obj, EligibilityPartOne.reasons_ineligible_fld_name))
        self.assertEqual(
            getattr(model_obj, EligibilityPartOne.eligible_fld_name),
            EligibilityPartOne.is_eligible_value,
        )

        self.screening_identifier = model_obj.screening_identifier

    def test_defaults_phase_three(self):
        self._test_defaults()

    def test_eligible_phase_three(self):
        self._test_eligible()

    def _test_defaults(self):

        obj = ScreeningPartTwo.objects.get(screening_identifier=self.screening_identifier)
        self.assertEqual(obj.eligible_part_two, TBD)
        self.assertIn("not answered", obj.reasons_ineligible_part_two)

        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

    def _test_eligible(self):

        obj = ScreeningPartTwo.objects.get(screening_identifier=self.screening_identifier)
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertIsNone(obj.reasons_ineligible_part_one)

        part_two_eligible_options = deepcopy(get_part_two_eligible_options())

        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)

        obj.advised_to_fast = NOT_APPLICABLE
        obj.appt_datetime = None
        obj.acute_condition = None
        obj.metformin_sensitivity = None
        obj.save()
        obj.refresh_from_db()

        self.assertIn("not answered", obj.reasons_ineligible_part_two)
        self.assertNotIn("Appt Datetime", obj.reasons_ineligible_part_two)
        self.assertNotIn("Advised To Fast", obj.reasons_ineligible_part_two)
        self.assertEqual(obj.eligible_part_two, TBD)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.acute_condition = NO
        obj.metformin_sensitivity = YES
        obj.save()

        self.assertIn(METFORMIN, (obj.reasons_ineligible_part_two or "").lower())
        self.assertEqual(obj.eligible_part_two, NO)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.acute_condition = NO
        obj.metformin_sensitivity = NO
        obj.advised_to_fast = YES
        obj.appt_datetime = get_utcnow() + relativedelta(days=1)
        obj.save()

        self.assertIsNone(obj.reasons_ineligible_part_two)
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)
