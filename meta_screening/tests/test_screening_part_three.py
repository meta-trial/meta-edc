from django.test import TestCase, tag
from edc_constants.constants import YES, BLACK, FEMALE, NOT_APPLICABLE, TBD, NO
from edc_reportable import (
    MICROMOLES_PER_LITER,
    MILLIMOLES_PER_LITER,
    ConversionNotHandled,
)
from edc_utils.date import get_utcnow

from ..constants import (
    EGFR_NOT_CALCULATED,
    BMI_IFT_OGTT,
    BMI_IFT_OGTT_INCOMPLETE,
    EGFR_LT_45,
)
from ..models import ScreeningPartOne, ScreeningPartTwo, ScreeningPartThree
from .options import part_two_eligible_options, part_three_eligible_options


class TestScreeningPartThree(TestCase):
    def setUp(self):
        obj = ScreeningPartOne(
            screening_consent=YES,
            report_datetime=get_utcnow(),
            hospital_identifier="111",
            initials="ZZ",
            gender=FEMALE,
            age_in_years=25,
            ethnicity=BLACK,
            hiv_pos=YES,
            art_six_months=YES,
            on_rx_stable=YES,
            lives_nearby=YES,
            staying_nearby=YES,
            pregnant=NOT_APPLICABLE,
        )
        obj.save()
        self.screening_identifier = obj.screening_identifier

        obj = ScreeningPartTwo.objects.get(
            screening_identifier=self.screening_identifier
        )
        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)
        obj.save()

    def test_defaults(self):

        obj = ScreeningPartThree.objects.get(
            screening_identifier=self.screening_identifier
        )
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertFalse(obj.reasons_ineligible_part_one)

        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.reasons_ineligible_part_two)

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertFalse(obj.reasons_ineligible_part_three)

        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

    def test_eligible(self):
        obj = ScreeningPartThree.objects.get(
            screening_identifier=self.screening_identifier
        )
        for k, v in part_three_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        self.assertEqual(obj.eligible_part_three, YES)

    def test_eligible_datetime_on_resave(self):
        obj = ScreeningPartThree.objects.get(
            screening_identifier=self.screening_identifier
        )
        for k, v in part_three_eligible_options.items():
            setattr(obj, k, v)
        obj.save()

        eligibility_datetime = obj.eligibility_datetime
        obj.save()
        self.assertNotEqual(eligibility_datetime, obj.eligibility_datetime)

    def test_eligible2(self):

        obj = ScreeningPartThree.objects.get(
            screening_identifier=self.screening_identifier
        )
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertFalse(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.reasons_ineligible_part_two)

        obj.part_three_report_datetime = get_utcnow()
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, BMI_IFT_OGTT_INCOMPLETE)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.part_three_report_datetime = get_utcnow()

        obj.weight = 65
        obj.height = 110
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, BMI_IFT_OGTT_INCOMPLETE)

        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.hba1c_performed = YES
        obj.hba1c = 7.0
        obj.creatinine_performed = NO
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, BMI_IFT_OGTT_INCOMPLETE)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.creatinine_performed = YES
        obj.creatinine = 50
        obj.creatinine_units = MICROMOLES_PER_LITER
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, BMI_IFT_OGTT_INCOMPLETE)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.fasted = NO
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, BMI_IFT_OGTT_INCOMPLETE)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.fasted = YES
        obj.fasted_duration_str = "8h"
        obj.fasting_glucose = 7.0
        obj.fasting_glucose_datetime = get_utcnow()
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertEqual(obj.reasons_ineligible_part_three, BMI_IFT_OGTT_INCOMPLETE)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.ogtt_base_datetime = get_utcnow()
        obj.ogtt_two_hr = 3.0
        obj.ogtt_two_hr_units = MICROMOLES_PER_LITER
        obj.ogtt_two_hr_datetime = get_utcnow()
        try:
            obj.save()
        except ConversionNotHandled:
            pass
        else:
            self.fail("ConversionNotHandled unexpectedly not raised.")

        obj.ogtt_two_hr_units = MILLIMOLES_PER_LITER
        obj.save()

        self.assertEqual(obj.eligible_part_three, NO)
        self.assertIn(BMI_IFT_OGTT, obj.reasons_ineligible_part_three)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.ogtt_base_datetime = get_utcnow()
        obj.ogtt_two_hr = 7.5
        obj.ogtt_two_hr_units = MILLIMOLES_PER_LITER
        obj.ogtt_two_hr_datetime = get_utcnow()
        obj.save()

        self.assertEqual(obj.eligible_part_three, YES)
        self.assertFalse(obj.reasons_ineligible_part_three)
        self.assertTrue(obj.eligible)
        self.assertFalse(obj.consented)

    def test_tbd_eligible_egfr_not_calculated(self):

        obj = ScreeningPartThree.objects.get(
            screening_identifier=self.screening_identifier
        )
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertFalse(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.reasons_ineligible_part_two)

        obj.part_three_report_datetime = get_utcnow()
        obj.part_three_report_datetime = get_utcnow()
        obj.weight = 65
        obj.height = 110
        obj.hba1c_performed = YES
        obj.hba1c = 7.0
        obj.creatinine_performed = NO
        #         obj.creatinine = 50
        #         obj.creatinine_units = MICROMOLES_PER_LITER
        obj.fasted = YES
        obj.fasted_duration_str = "8h"
        obj.fasting_glucose = 7.0
        obj.fasting_glucose_units = MILLIMOLES_PER_LITER
        obj.fasting_glucose_datetime = get_utcnow()
        obj.ogtt_base_datetime = get_utcnow()
        obj.ogtt_two_hr = 7.5
        obj.ogtt_two_hr_units = MILLIMOLES_PER_LITER
        obj.ogtt_two_hr_datetime = get_utcnow()
        obj.save()

        self.assertEqual(obj.eligible_part_three, TBD)
        self.assertIn(EGFR_NOT_CALCULATED, obj.reasons_ineligible_part_three)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

    def test_not_eligible_egfr_less_than_45(self):

        obj = ScreeningPartThree.objects.get(
            screening_identifier=self.screening_identifier
        )
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertFalse(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.reasons_ineligible_part_two)

        obj.part_three_report_datetime = get_utcnow()
        obj.part_three_report_datetime = get_utcnow()
        obj.weight = 65
        obj.height = 110
        obj.hba1c_performed = YES
        obj.hba1c = 7.0
        obj.creatinine_performed = NO
        obj.creatinine = 200
        obj.creatinine_units = MICROMOLES_PER_LITER
        obj.fasted = YES
        obj.fasted_duration_str = "8h"
        obj.fasting_glucose = 7.0
        obj.fasting_glucose_datetime = get_utcnow()
        obj.ogtt_base_datetime = get_utcnow()
        obj.ogtt_two_hr = 7.5
        obj.ogtt_two_hr_units = MILLIMOLES_PER_LITER
        obj.ogtt_two_hr_datetime = get_utcnow()
        obj.save()

        self.assertEqual(obj.eligible_part_three, NO)
        self.assertIn(EGFR_LT_45, obj.reasons_ineligible_part_three)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)
