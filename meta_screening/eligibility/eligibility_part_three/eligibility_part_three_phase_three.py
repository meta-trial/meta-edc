from edc_constants.constants import NO, TBD, YES
from edc_reportable import calculate_egfr

from ...constants import EGFR_LT_45, IFT_OGTT, IFT_OGTT_INCOMPLETE, SEVERE_HTN
from .base_eligibility_part_three import BaseEligibilityPartThree


class EligibilityPartThreePhaseThree(BaseEligibilityPartThree):
    def assess_eligibility(self):
        super().assess_eligibility()
        a, b = self.calculate_inclusion_field_values()
        self.obj.inclusion_a = a
        self.obj.inclusion_b = b
        reasons_ineligible = []
        if a == TBD or b == TBD:
            reasons_ineligible.append(IFT_OGTT_INCOMPLETE)
            self.obj.eligible_part_three = TBD
        if a == NO and b == NO:
            reasons_ineligible.append(IFT_OGTT)
            self.obj.eligible_part_three = NO
        if self.obj.severe_htn == YES:
            reasons_ineligible.append(SEVERE_HTN)
        if not reasons_ineligible:
            self.obj.calculated_egfr_value = calculate_egfr(**self.obj.__dict__)
            if self.obj.calculated_egfr_value and self.obj.calculated_egfr_value < 45.0:
                reasons_ineligible.append(EGFR_LT_45)
                self.obj.eligible_part_three = NO
        if not reasons_ineligible:
            self.obj.eligible_part_three = YES
            self.obj.eligibility_datetime = self.obj.part_three_report_datetime
        elif IFT_OGTT_INCOMPLETE not in reasons_ineligible:
            self.obj.eligible_part_three = NO
            self.obj.eligibility_datetime = None
        self.obj.reasons_ineligible_part_three = "|".join(reasons_ineligible)

    def calculate_inclusion_field_values(self):
        # IFG (6.1 to 6.9 mmol/L)
        if not self.obj.converted_ifg_value:
            inclusion_a = TBD
        elif 6.1 <= self.obj.converted_ifg_value <= 6.9:
            inclusion_a = YES
        else:
            inclusion_a = NO

        # OGTT (7.8 to 11.10 mmol/L)
        if not self.obj.converted_ogtt_value:
            inclusion_b = TBD
        elif 7.8 <= self.obj.converted_ogtt_value <= 11.10:
            inclusion_b = YES
        else:
            inclusion_b = NO

        return inclusion_a, inclusion_b
