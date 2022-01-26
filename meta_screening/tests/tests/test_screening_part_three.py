from copy import deepcopy
from unittest import skipIf

from django.test import TestCase
from edc_constants.constants import NO, TBD, YES
from edc_reportable import (
    MICROMOLES_PER_LITER,
    MILLIMOLES_PER_LITER,
    ConversionNotHandled,
)
from edc_utils.date import get_utcnow

from meta_edc.meta_version import PHASE_THREE, PHASE_TWO, get_meta_version
from meta_screening.constants import (
    BMI_IFT_OGTT,
    BMI_IFT_OGTT_INCOMPLETE,
    EGFR_LT_45,
    EGFR_NOT_CALCULATED,
    IFT_OGTT,
    IFT_OGTT_INCOMPLETE,
)
from meta_screening.models import ScreeningPartOne, ScreeningPartThree, ScreeningPartTwo

from ..options import (
    get_part_one_eligible_options,
    get_part_three_eligible_options,
    get_part_two_eligible_options,
)


class TestScreeningPartThree(TestCase):
    def setUp(self):
        """Complete parts one and two first ..."""
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        obj = ScreeningPartOne(**part_one_eligible_options)
        obj.save()
        obj.refresh_from_db()
        self.screening_identifier = obj.screening_identifier

        obj = ScreeningPartTwo.objects.get(
            screening_identifier=self.screening_identifier
        )
        for k, v in part_two_eligible_options.items():
            getattr(obj, k)
            setattr(obj, k, v)
        obj.save()
        obj.refresh_from_db()

        # assert eligible for part one criteria
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertIsNone(obj.reasons_ineligible_part_one)

        # assert eligible for part two criteria
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertIsNone(obj.reasons_ineligible_part_two)

        # assert eligiblility to be determined for part three
        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertIsNotNone(obj.reasons_ineligible_part_three)

        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

    def get_screening_part_three_obj(self):
        """Returns an SubjectScreening obj.

        Remember this is just a proxy model for SubjectScreening.
        """
        return ScreeningPartThree.objects.get(
            screening_identifier=self.screening_identifier,
        )

    @skipIf(get_meta_version() != PHASE_TWO, "not META2")
    def test_eligible_part_three_defaults_phase_two(self):
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        self._test_eligible(part_three_eligible_options)

    @skipIf(get_meta_version() != PHASE_THREE, "not META3")
    def test_eligible_part_three_defaults_phase_three(self):
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        part_three_eligible_options["ifg_value"] = 6.9
        part_three_eligible_options["ogtt_value"] = 7.8
        self._test_eligible(part_three_eligible_options)

    def _test_eligible(self, part_three_eligible_options):
        obj = self.get_screening_part_three_obj()
        for k, v in part_three_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        self.assertIsNone(obj.reasons_ineligible_part_three)
        self.assertEqual(obj.eligible_part_three, YES)

    def test_eligible_datetime_does_not_change_on_resave(self):
        obj = self.get_screening_part_three_obj()
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        for k, v in part_three_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        obj.refresh_from_db()
        eligibility_datetime = obj.eligibility_datetime
        obj.save()
        obj.refresh_from_db()
        self.assertEqual(eligibility_datetime, obj.eligibility_datetime)

    @skipIf(get_meta_version() != PHASE_TWO, "not META2")
    def test_eligible2_phase_two(self):
        obj = self.get_screening_part_three_obj()
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        for k, v in part_three_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        obj.refresh_from_db()
        self.assertIsNone(obj.reasons_ineligible_part_three)
        self.assertEqual(obj.eligible_part_three, YES)
        obj.ogtt_base_datetime = None
        obj.ogtt_datetime = None
        obj.ogtt_units = None
        obj.ogtt_value = None
        obj.save()
        obj.refresh_from_db()
        self._test_eligible2(obj, BMI_IFT_OGTT_INCOMPLETE, BMI_IFT_OGTT)

    @skipIf(get_meta_version() != PHASE_THREE, "not META3")
    def test_eligible2_phase_three(self):
        obj = self.get_screening_part_three_obj()
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        for k, v in part_three_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        obj.refresh_from_db()
        self.assertIsNone(obj.reasons_ineligible_part_three)
        self.assertEqual(obj.eligible_part_three, YES)
        obj.severe_htn = YES
        obj.save()
        obj.refresh_from_db()
        self.assertIn("Severe HTN", obj.reasons_ineligible_part_three)
        self.assertEqual(obj.eligible_part_three, NO)
        obj.severe_htn = NO
        obj.save()
        obj.refresh_from_db()
        self.assertIsNone(obj.reasons_ineligible_part_three)
        self.assertEqual(obj.eligible_part_three, YES)
        obj.ogtt_base_datetime = None
        obj.ogtt_datetime = None
        obj.ogtt_units = None
        obj.ogtt_value = None
        obj.save()
        obj.refresh_from_db()
        self._test_eligible2(obj, IFT_OGTT_INCOMPLETE, IFT_OGTT)

    def _test_eligible2(self, obj, incomplete_reason: str, ineligible_reason: str):
        self.assertIsNone(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertIsNone(obj.reasons_ineligible_part_two)
        self.assertEqual(obj.eligible_part_two, YES)

        self.assertEqual(obj.reasons_ineligible_part_three, incomplete_reason)
        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.hba1c_performed = YES
        obj.hba1c_value = 7.0
        obj.creatinine_performed = NO
        obj.save()

        self.assertEqual(obj.reasons_ineligible_part_three, incomplete_reason)
        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.creatinine_performed = YES
        obj.creatinine_value = 50
        obj.creatinine_units = MICROMOLES_PER_LITER
        obj.save()

        self.assertEqual(obj.reasons_ineligible_part_three, incomplete_reason)
        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.fasting = NO
        obj.save()

        self.assertEqual(obj.reasons_ineligible_part_three, incomplete_reason)
        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.fasting = YES
        obj.fasting_duration_str = "8h"
        obj.ifg_value = 6.9
        obj.ifg_units = MILLIMOLES_PER_LITER
        obj.ifg_datetime = get_utcnow()
        obj.save()

        self.assertEqual(obj.reasons_ineligible_part_three, incomplete_reason)
        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.ogtt_base_datetime = get_utcnow()
        obj.ogtt_value = 3.0
        obj.ogtt_units = MICROMOLES_PER_LITER
        obj.ogtt_datetime = get_utcnow()
        try:
            obj.save()
        except ConversionNotHandled:
            pass
        else:
            self.fail("ConversionNotHandled unexpectedly not raised.")

        obj.refresh_from_db()
        obj.ogtt_units = MILLIMOLES_PER_LITER
        obj.save()

        self.assertIn(ineligible_reason, obj.reasons_ineligible_part_three)
        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.ogtt_base_datetime = get_utcnow()
        obj.ogtt_value = 7.8
        obj.ogtt_units = MILLIMOLES_PER_LITER
        obj.ogtt_datetime = get_utcnow()
        obj.save()

        self.assertFalse(obj.reasons_ineligible_part_three)
        self.assertEqual(obj.eligible_part_three, YES)
        self.assertTrue(obj.eligible)
        self.assertFalse(obj.consented)

    @skipIf(get_meta_version() != PHASE_TWO, "not META2")
    def test_tbd_eligible_egfr_not_calculated_phase_two(self):
        ifg_value = 7.0
        ogtt_value = 7.5
        obj = self._test_egfr_not_calculated(ifg_value, ogtt_value)
        self.assertIn(EGFR_NOT_CALCULATED, obj.reasons_ineligible_part_three)
        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

    @skipIf(get_meta_version() != PHASE_THREE, "not META3")
    def test_yes_eligible_egfr_not_calculated_phase_three(self):
        """Is eligible, since phase three will allow for EGFR to be considered
        late exclusion.
        """
        ifg_value = 6.9
        ogtt_value = 7.8
        obj = self._test_egfr_not_calculated(ifg_value, ogtt_value)
        self.assertNotIn(EGFR_NOT_CALCULATED, obj.reasons_ineligible_part_three or "")
        self.assertEqual(obj.eligible_part_three, YES)
        self.assertTrue(obj.eligible)
        self.assertFalse(obj.consented)

    def _test_egfr_not_calculated(self, ifg_value, ogtt_value):
        obj = self.get_screening_part_three_obj()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertFalse(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.reasons_ineligible_part_two)

        obj.ifg_value = ifg_value
        obj.ogtt_value = ogtt_value

        obj.part_three_report_datetime = get_utcnow()
        obj.weight = 65
        obj.height = 110
        obj.hba1c_performed = YES
        obj.hba1c_value = 7.0
        obj.creatinine_performed = NO
        obj.fasting = YES
        obj.fasting_duration_str = "8h"
        obj.ifg_units = MILLIMOLES_PER_LITER
        obj.ifg_datetime = get_utcnow()
        obj.ogtt_base_datetime = get_utcnow()
        obj.ogtt_units = MILLIMOLES_PER_LITER
        obj.ogtt_datetime = get_utcnow()
        obj.severe_htn = NO
        obj.save()
        return obj

    @skipIf(get_meta_version() != PHASE_TWO, "not META2")
    def test_not_eligible_egfr_less_than_45_phase_two(self):
        ifg_value = 7.0
        ogtt_value = 7.5
        self._test_not_eligible_egfr_less_than_45(ifg_value, ogtt_value)

    @skipIf(get_meta_version() != PHASE_THREE, "not META3")
    def test_not_eligible_egfr_less_than_45_phase_three(self):
        ifg_value = 6.9
        ogtt_value = 7.8
        self._test_not_eligible_egfr_less_than_45(ifg_value, ogtt_value)

    def _test_not_eligible_egfr_less_than_45(self, ifg_value, ogtt_value):

        obj = self.get_screening_part_three_obj()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertFalse(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.reasons_ineligible_part_two)

        obj.ifg_value = ifg_value
        obj.ogtt_value = ogtt_value

        # defaults
        obj.creatinine_performed = NO
        obj.creatinine_units = MICROMOLES_PER_LITER
        obj.creatinine_value = 200
        obj.fasting = YES
        obj.fasting_duration_str = "8h"
        obj.hba1c_performed = YES
        obj.hba1c_value = 7.0
        obj.height = 110
        obj.ifg_datetime = get_utcnow()
        obj.ifg_units = MILLIMOLES_PER_LITER
        obj.ogtt_base_datetime = get_utcnow()
        obj.ogtt_datetime = get_utcnow()
        obj.ogtt_units = MILLIMOLES_PER_LITER
        obj.part_three_report_datetime = get_utcnow()
        obj.severe_htn = NO
        obj.weight = 65
        obj.save()

        self.assertIn(EGFR_LT_45, obj.reasons_ineligible_part_three)
        self.assertEqual(obj.eligible_part_three, NO)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)
