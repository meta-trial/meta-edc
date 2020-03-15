from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, tag
from edc_constants.constants import YES, BLACK, FEMALE, NOT_APPLICABLE, NO
from edc_reportable.units import MICROMOLES_PER_LITER, MILLIMOLES_PER_LITER
from edc_utils.date import get_utcnow

from ..models import IcpReferral, ScreeningPartOne, ScreeningPartTwo, ScreeningPartThree
from ..signals import refer_to_icp


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
        obj.part_two_report_datetime = get_utcnow()
        obj.urine_bhcg_performed = NO
        obj.congestive_heart_failure = NO
        obj.liver_disease = NO
        obj.alcoholism = NO
        obj.acute_metabolic_acidosis = NO
        obj.renal_function_condition = NO
        obj.tissue_hypoxia_condition = NO
        obj.acute_condition = NO
        obj.metformin_sensitivity = NO
        obj.advised_to_fast = YES
        obj.appt_datetime = get_utcnow() + relativedelta(days=1)
        obj.save()

    def test_creates_icp_referral(self):
        obj = ScreeningPartThree.objects.get(
            screening_identifier=self.screening_identifier
        )

        self.assertEqual(obj.eligible_part_one, YES)
        self.assertFalse(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertFalse(obj.reasons_ineligible_part_two)

        obj.part_three_report_datetime = get_utcnow()
        obj.weight = 65
        obj.height = 110
        obj.hba1c_performed = YES
        obj.hba1c = 7.0
        obj.creatinine_performed = YES
        obj.creatinine = 100
        obj.creatinine_units = MICROMOLES_PER_LITER
        obj.fasted = YES
        obj.fasted_duration_str = "8h"
        obj.fasting_glucose = 7.5
        obj.fasting_glucose_datetime = get_utcnow()
        obj.ogtt_base_datetime = get_utcnow()
        obj.ogtt_two_hr = 12.0
        obj.ogtt_two_hr_units = MILLIMOLES_PER_LITER
        obj.ogtt_two_hr_datetime = get_utcnow()
        obj.save()

        self.assertTrue(obj.reasons_ineligible_part_three)
        self.assertEqual(obj.eligible_part_three, NO)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        self.assertTrue(refer_to_icp(obj))

        try:
            IcpReferral.objects.get(subject_screening=obj)
        except ObjectDoesNotExist as e:
            self.fail(f"ObjectDoesNotExist unexpectedly raised. Got {e}")
