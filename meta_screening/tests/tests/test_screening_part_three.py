from copy import deepcopy

from django.test import TestCase, override_settings, tag
from edc_constants.constants import NO, TBD, YES
from edc_reportable import (
    MICROMOLES_PER_LITER,
    MILLIMOLES_PER_LITER,
    ConversionNotHandled,
)
from edc_utils.date import get_utcnow

from meta_edc.meta_version import PHASE_THREE, PHASE_TWO
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


@tag("el")
class TestScreeningPartThree(TestCase):
    def setUp(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        obj = ScreeningPartOne(**part_one_eligible_options)
        obj.save()
        self.screening_identifier = obj.screening_identifier

        obj = ScreeningPartTwo.objects.get(
            screening_identifier=self.screening_identifier
        )
        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)
        obj.save()

    def get_screening_part_three_obj(self):
        return ScreeningPartThree.objects.get(
            screening_identifier=self.screening_identifier
        )

    def test_defaults(self):
        obj = self.get_screening_part_three_obj()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertFalse(obj.reasons_ineligible_part_one)

        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.reasons_ineligible_part_two)

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertFalse(obj.reasons_ineligible_part_three)

        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

    @tag("99")
    @override_settings(META_PHASE=PHASE_TWO)
    def test_eligible_phase_two(self):
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        self._test_eligible(part_three_eligible_options)

    @override_settings(META_PHASE=PHASE_THREE)
    def test_eligible_phase_three(self):
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        part_three_eligible_options["ifg_value"] = 6.9
        part_three_eligible_options["ogtt_value"] = 7.8
        self._test_eligible(part_three_eligible_options)

    def _test_eligible(self, part_three_eligible_options):
        obj = self.get_screening_part_three_obj()
        for k, v in part_three_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        self.assertEqual("", obj.reasons_ineligible_part_three)
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

    @override_settings(META_PHASE=PHASE_TWO)
    def test_eligible2_phase_two(self):
        self._test_eligible2(BMI_IFT_OGTT_INCOMPLETE, BMI_IFT_OGTT)

    @override_settings(META_PHASE=PHASE_THREE)
    def test_eligible2_phase_three(self):
        self._test_eligible2(IFT_OGTT_INCOMPLETE, IFT_OGTT)

    def _test_eligible2(self, incomplete_reason, ineligible_reason):
        obj = self.get_screening_part_three_obj()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertFalse(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.reasons_ineligible_part_two)

        obj.part_three_report_datetime = get_utcnow()
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, incomplete_reason)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.part_three_report_datetime = get_utcnow()

        obj.weight = 65
        obj.height = 110
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, incomplete_reason)

        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.hba1c_performed = YES
        obj.hba1c_value = 7.0
        obj.creatinine_performed = NO
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, incomplete_reason)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.creatinine_performed = YES
        obj.creatinine_value = 50
        obj.creatinine_units = MICROMOLES_PER_LITER
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, incomplete_reason)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.fasting = NO
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, incomplete_reason)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.fasting = YES
        obj.fasting_duration_str = "8h"
        obj.ifg_value = 7.0
        obj.ifg_units = MILLIMOLES_PER_LITER
        obj.ifg_datetime = get_utcnow()
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, incomplete_reason)
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

        obj.ogtt_units = MILLIMOLES_PER_LITER
        obj.save()

        self.assertEqual(obj.eligible_part_three, NO)
        self.assertIn(ineligible_reason, obj.reasons_ineligible_part_three)
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

    @override_settings(META_PHASE=PHASE_TWO)
    def test_tbd_eligible_egfr_not_calculated_phase_two(self):
        ifg_value = 7.0
        ogtt_value = 7.5
        obj = self._test_egfr_not_calculated(ifg_value, ogtt_value)
        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertIn(EGFR_NOT_CALCULATED, obj.reasons_ineligible_part_three)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

    @override_settings(META_PHASE=PHASE_THREE)
    def test_yes_eligible_egfr_not_calculated_phase_three(self):
        """Is eligible, since phase three will allow for EGFR to be considered
        late exclusion.
        """
        ifg_value = 6.9
        ogtt_value = 7.8
        obj = self._test_egfr_not_calculated(ifg_value, ogtt_value)
        self.assertEqual(obj.eligible_part_three, YES)
        self.assertNotIn(EGFR_NOT_CALCULATED, obj.reasons_ineligible_part_three)
        self.assertTrue(obj.eligible)
        self.assertFalse(obj.consented)

    def _test_egfr_not_calculated(self, ifg_value, ogtt_value):
        obj = self.get_screening_part_three_obj()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertFalse(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.reasons_ineligible_part_two)
        obj.part_three_report_datetime = get_utcnow()
        obj.part_three_report_datetime = get_utcnow()
        obj.weight = 65
        obj.height = 110
        obj.hba1c_performed = YES
        obj.hba1c_value = 7.0
        obj.creatinine_performed = NO
        obj.fasting = YES
        obj.fasting_duration_str = "8h"
        obj.ifg_value = ifg_value
        obj.ifg_units = MILLIMOLES_PER_LITER
        obj.ifg_datetime = get_utcnow()
        obj.ogtt_base_datetime = get_utcnow()
        obj.ogtt_value = ogtt_value
        obj.ogtt_units = MILLIMOLES_PER_LITER
        obj.ogtt_datetime = get_utcnow()
        obj.save()
        return obj

    @override_settings(META_PHASE=PHASE_TWO)
    def test_not_eligible_egfr_less_than_45_phase_two(self):
        ifg_value = 7.0
        ogtt_value = 7.5
        self._test_not_eligible_egfr_less_than_45(ifg_value, ogtt_value)

    @override_settings(META_PHASE=PHASE_THREE)
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

        obj.part_three_report_datetime = get_utcnow()
        obj.part_three_report_datetime = get_utcnow()
        obj.weight = 65
        obj.height = 110
        obj.hba1c_performed = YES
        obj.hba1c_value = 7.0
        obj.creatinine_performed = NO
        obj.creatinine_value = 200
        obj.creatinine_units = MICROMOLES_PER_LITER
        obj.fasting = YES
        obj.fasting_duration_str = "8h"
        obj.ifg_value = ifg_value
        obj.ifg_units = MILLIMOLES_PER_LITER
        obj.ifg_datetime = get_utcnow()
        obj.ogtt_base_datetime = get_utcnow()
        obj.ogtt_value = ogtt_value
        obj.ogtt_units = MILLIMOLES_PER_LITER
        obj.ogtt_datetime = get_utcnow()
        obj.save()

        self.assertEqual(obj.eligible_part_three, NO)
        self.assertIn(EGFR_LT_45, obj.reasons_ineligible_part_three)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)
