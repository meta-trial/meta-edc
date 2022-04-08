from edc_constants.constants import NO, NOT_APPLICABLE, PENDING, TBD, YES
from edc_screening.screening_eligibility import FC, ScreeningEligibilityError

from ...constants import EGFR_LT_45, FBG_OGTT_INCOMPLETE, IFT_OGTT, SEVERE_HTN
from .base_eligibility_part_three import BaseEligibilityPartThree


class EligibilityPartThreePhaseThree(BaseEligibilityPartThree):
    def __init__(self, **kwargs):
        self.inclusion_a = TBD
        self.inclusion_b = TBD
        self.severe_htn = None
        super().__init__(**kwargs)

    def assess_eligibility(self) -> None:
        """Subject is eligible if either a qualifying FBG OR a qualifying OGTT"""
        # TODO: check if calculates correctly if glucose is HIGH 9999.99
        super().assess_eligibility()
        self.calculate_inclusion_field_values()
        if self.inclusion_a == TBD or self.inclusion_b == TBD:
            self.reasons_ineligible.update(fbg_ogtt=FBG_OGTT_INCOMPLETE)
            self.eligible = TBD
        elif self.inclusion_a == NO and self.inclusion_b == NO:
            self.reasons_ineligible.update(fbg_ogtt=IFT_OGTT)
            self.eligible = NO
        elif self.calculated_egfr_value and self.calculated_egfr_value < 45.0:
            self.reasons_ineligible.update(egfr=EGFR_LT_45)
            self.eligible = NO

    def set_fld_attrs_on_model(self) -> None:
        """Set extra attr on the model"""
        super().set_fld_attrs_on_model()
        self.model_obj.inclusion_a = self.inclusion_a
        self.model_obj.inclusion_b = self.inclusion_b
        self.model_obj.inclusion_c = NOT_APPLICABLE
        self.model_obj.inclusion_d = NOT_APPLICABLE

    def get_required_fields(self) -> dict[str, FC]:
        """Get default fields as well as severe_htn"""
        fields = super().get_required_fields()
        fields.update({"severe_htn": FC(NO, SEVERE_HTN)})
        return fields

    def calculate_inclusion_field_values(self) -> None:
        """Decide which values to use, first or repeat"""
        if self.repeat_glucose_performed == PENDING:
            self.inclusion_a = TBD
            self.inclusion_b = TBD
        else:
            converted_fbg_value = (
                self.converted_fbg2_value
                if self.repeat_glucose_opinion == YES
                else self.converted_fbg_value
            )
            converted_ogtt_value = (
                self.converted_ogtt2_value
                if self.repeat_glucose_opinion == YES
                else self.converted_ogtt_value
            )
            # FBG (6.1 to 6.9 mmol/L)
            # TODO ensure only 1 decimal place is reported on the form
            if not converted_fbg_value:
                self.inclusion_a = TBD
            elif 6.1 <= converted_fbg_value < 7.0:
                self.inclusion_a = YES
            else:
                self.inclusion_a = NO

            # OGTT (7.8 to 11.10 mmol/L)
            if not converted_ogtt_value:
                self.inclusion_b = TBD
            elif 7.8 <= converted_ogtt_value < 11.1:
                self.inclusion_b = YES
            else:
                self.inclusion_b = NO
