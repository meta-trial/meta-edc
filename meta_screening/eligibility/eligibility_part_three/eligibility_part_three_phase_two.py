from edc_constants.constants import NO, TBD, YES
from edc_reportable import calculate_egfr
from edc_screening.screening_eligibility import ScreeningEligibilityError

from meta_edc.meta_version import PHASE_TWO, get_meta_version

from ...constants import (
    BMI_FBG_OGTT_INCOMPLETE,
    BMI_IFT_OGTT,
    EGFR_LT_45,
    EGFR_NOT_CALCULATED,
)
from .base_eligibility_part_three import BaseEligibilityPartThree


class EligibilityPartThreePhaseTwo(BaseEligibilityPartThree):
    def __init__(self, **kwargs):
        if get_meta_version() != PHASE_TWO:
            raise ScreeningEligibilityError(
                f"Invalid META Phase. Expected {PHASE_TWO}. Got {get_meta_version()}"
            )
        self.inclusion_a = TBD
        self.inclusion_b = TBD
        self.inclusion_c = TBD
        self.inclusion_d = TBD
        super().__init__(**kwargs)

    def assess_eligibility(self) -> None:
        super().assess_eligibility()
        a, b, c, d = self.calculate_inclusion_field_values()
        self.inclusion_a = a
        self.inclusion_b = b
        self.inclusion_c = c
        self.inclusion_d = d
        if a == NO and b == NO and c == NO and d == NO:
            self.reasons_ineligible.update({"bmi_ift_ogtt": BMI_IFT_OGTT})
            self.eligible = NO
        elif a == TBD or b == TBD or c == TBD or d == TBD:
            self.reasons_ineligible.update({"bmi_ift_ogtt": BMI_FBG_OGTT_INCOMPLETE})
            self.eligible = TBD
        if not self.reasons_ineligible:
            self.model_obj.calculated_egfr_value = calculate_egfr(
                **self.model_obj.__dict__
            )
            if not self.model_obj.calculated_egfr_value:
                self.reasons_ineligible.update({"egfr": EGFR_NOT_CALCULATED})
                self.eligible = TBD
            elif self.calculated_egfr_value < 45.0:
                self.reasons_ineligible.update({"egfr": EGFR_LT_45})
                self.eligible = NO
        if not self.reasons_ineligible:
            self.eligible = YES
        elif (
            BMI_FBG_OGTT_INCOMPLETE not in self.reasons_ineligible.values()
            and EGFR_NOT_CALCULATED not in self.reasons_ineligible.values()
        ):
            self.eligible = NO

    def set_fld_attrs_on_model(self) -> None:
        super().set_fld_attrs_on_model()
        self.model_obj.inclusion_a = self.inclusion_a
        self.model_obj.inclusion_b = self.inclusion_b
        self.model_obj.inclusion_c = self.inclusion_c
        self.model_obj.inclusion_d = self.inclusion_d

    def calculate_inclusion_field_values(self):
        # (a) BMI > 30 combined with IFG (6.1 to 6.9 mmol/L)
        if self.bmi.value is None or not self.converted_fbg_value:
            inclusion_a = TBD
        elif self.bmi.value > 30.0 and 6.1 <= self.converted_fbg_value <= 6.9:
            inclusion_a = YES
        else:
            inclusion_a = NO

        # (b) BMI > 30 combined with OGTT (7.0 to 11.10 mmol/L)
        if self.bmi.value is None or not self.converted_ogtt_value:
            inclusion_b = TBD
        elif self.bmi.value > 30.0 and 7.0 <= self.converted_ogtt_value <= 11.10:
            inclusion_b = YES
        else:
            inclusion_b = NO

        # (c) BMI <= 30 combined with IFG (6.3 to 6.9 mmol/L)
        if self.bmi.value is None or not self.converted_fbg_value:
            inclusion_c = TBD
        elif self.bmi.value <= 30.0 and 6.3 <= self.converted_fbg_value <= 6.9:
            inclusion_c = YES
        else:
            inclusion_c = NO

        # (d) BMI <= 30 combined with OGTT (9.0 to 11.10 mmol/L)
        if self.bmi.value is None or not self.converted_ogtt_value:
            inclusion_d = TBD
        elif self.bmi.value <= 30.0 and 9.0 <= self.converted_ogtt_value <= 11.10:
            inclusion_d = YES
        else:
            inclusion_d = NO
        return inclusion_a, inclusion_b, inclusion_c, inclusion_d
