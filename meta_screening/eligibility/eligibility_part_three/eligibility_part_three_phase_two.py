from edc_constants.constants import NO, TBD, YES
from edc_reportable import calculate_egfr

from ...constants import (
    BMI_IFT_OGTT,
    BMI_IFT_OGTT_INCOMPLETE,
    EGFR_LT_45,
    EGFR_NOT_CALCULATED,
)
from .base_eligibility_part_three import BaseEligibilityPartThree


class EligibilityPartThreePhaseTwo(BaseEligibilityPartThree):
    def assess_eligibility(self):
        super().assess_eligibility()
        a, b, c, d = self.calculate_inclusion_field_values()
        self.obj.inclusion_a = a
        self.obj.inclusion_b = b
        self.obj.inclusion_c = c
        self.obj.inclusion_d = d
        reasons_ineligible = self.get_reasons_ineligible(a, b, c, d)
        if not reasons_ineligible:
            self.obj.eligible_part_three = YES
        elif (
            BMI_IFT_OGTT_INCOMPLETE not in reasons_ineligible
            and EGFR_NOT_CALCULATED not in reasons_ineligible
        ):
            self.obj.eligible_part_three = NO
        self.obj.reasons_ineligible_part_three = "|".join(reasons_ineligible)

    def get_reasons_ineligible(self, a, b, c, d):
        reasons_ineligible = []
        if a == TBD or b == TBD or c == TBD or d == TBD:
            reasons_ineligible.append(BMI_IFT_OGTT_INCOMPLETE)
            self.obj.eligible_part_three = TBD
        if a == NO and b == NO and c == NO and d == NO:
            reasons_ineligible.append(BMI_IFT_OGTT)
            self.obj.eligible_part_three = NO
        if not reasons_ineligible:
            self.obj.calculated_egfr_value = calculate_egfr(**self.obj.__dict__)
            if not self.obj.calculated_egfr_value:
                reasons_ineligible.append(EGFR_NOT_CALCULATED)
                self.obj.eligible_part_three = TBD
            elif self.obj.calculated_egfr_value < 45.0:
                reasons_ineligible.append(EGFR_LT_45)
                self.obj.eligible_part_three = NO
        return reasons_ineligible

    def calculate_inclusion_field_values(self):
        # (a) BMI > 30 combined with IFG (6.1 to 6.9 mmol/L)
        if self.obj.calculated_bmi_value is None or not self.obj.converted_ifg_value:
            inclusion_a = TBD
        elif (
            self.obj.calculated_bmi_value > 30.0
            and 6.1 <= self.obj.converted_ifg_value <= 6.9
        ):
            inclusion_a = YES
        else:
            inclusion_a = NO

        # (b) BMI > 30 combined with OGTT (7.0 to 11.10 mmol/L)
        if self.obj.calculated_bmi_value is None or not self.obj.converted_ogtt_value:
            inclusion_b = TBD
        elif (
            self.obj.calculated_bmi_value > 30.0
            and 7.0 <= self.obj.converted_ogtt_value <= 11.10
        ):
            inclusion_b = YES
        else:
            inclusion_b = NO

        # (c) BMI <= 30 combined with IFG (6.3 to 6.9 mmol/L)
        if self.obj.calculated_bmi_value is None or not self.obj.converted_ifg_value:
            inclusion_c = TBD
        elif (
            self.obj.calculated_bmi_value <= 30.0
            and 6.3 <= self.obj.converted_ifg_value <= 6.9
        ):
            inclusion_c = YES
        else:
            inclusion_c = NO

        # (d) BMI <= 30 combined with OGTT (9.0 to 11.10 mmol/L)
        if self.obj.calculated_bmi_value is None or not self.obj.converted_ogtt_value:
            inclusion_d = TBD
        elif (
            self.obj.calculated_bmi_value <= 30.0
            and 9.0 <= self.obj.converted_ogtt_value <= 11.10
        ):
            inclusion_d = YES
        else:
            inclusion_d = NO

        return inclusion_a, inclusion_b, inclusion_c, inclusion_d
