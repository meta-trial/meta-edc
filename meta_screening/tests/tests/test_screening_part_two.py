from copy import deepcopy

from dateutil.relativedelta import relativedelta
from django.test import TestCase, override_settings, tag
from edc_constants.constants import NO, TBD, YES
from edc_utils.date import get_utcnow

from meta_edc.meta_version import PHASE_THREE, PHASE_TWO
from meta_screening.models import ScreeningPartOne, ScreeningPartTwo

from ..options import get_part_one_eligible_options, get_part_two_eligible_options


@tag("el")
class TestScreeningPartTwo(TestCase):
    def setUp(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        self.screening = ScreeningPartOne(**part_one_eligible_options)
        self.screening.save()
        self.screening_identifier = self.screening.screening_identifier

    @override_settings(META_PHASE=PHASE_TWO)
    def test_defaults_phase_two(self):
        self._test_defaults()

    @override_settings(META_PHASE=PHASE_THREE)
    def test_defaults_phase_three(self):
        self._test_defaults()

    @override_settings(META_PHASE=PHASE_TWO)
    def test_eligible_phase_two(self):
        self._test_eligible()

    @override_settings(META_PHASE=PHASE_THREE)
    def test_eligible_phase_three(self):
        self._test_eligible()

    def _test_defaults(self):

        obj = ScreeningPartTwo.objects.get(
            screening_identifier=self.screening_identifier
        )
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertTrue(obj.reasons_ineligible_part_one == "")

        self.assertEqual(obj.eligible_part_two, TBD)
        self.assertFalse(obj.reasons_ineligible_part_two)

        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

    def _test_eligible(self):

        obj = ScreeningPartTwo.objects.get(
            screening_identifier=self.screening_identifier
        )
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())

        self.assertEqual(obj.eligible_part_one, YES)
        self.assertTrue(obj.reasons_ineligible_part_one == "")

        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)
        obj.acute_condition = None
        obj.metformin_sensitivity = None
        obj.advised_to_fast = NO
        obj.appt_datetime = None
        obj.save()

        self.assertEqual(obj.eligible_part_two, TBD)
        self.assertFalse(obj.reasons_ineligible_part_two)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.acute_condition = NO
        obj.metformin_sensitivity = YES
        obj.save()

        self.assertEqual(obj.eligible_part_two, NO)
        self.assertIn("Metformin", obj.reasons_ineligible_part_two)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.acute_condition = NO
        obj.metformin_sensitivity = NO
        obj.advised_to_fast = YES
        obj.appt_datetime = get_utcnow() + relativedelta(days=1)
        obj.save()

        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.reasons_ineligible_part_two)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)
