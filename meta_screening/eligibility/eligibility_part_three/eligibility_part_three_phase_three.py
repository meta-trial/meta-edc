from typing import Any

from edc_constants.constants import DM, NO, NORMAL, NOT_APPLICABLE, PENDING, TBD, YES
from edc_screening.screening_eligibility import FC

from ...constants import (
    EGFR_LT_45,
    FBG_OGTT_INCOMPLETE,
    HI_FBG,
    HI_OGTT,
    NORMAL_FBG_OGTT,
    PRE_DM,
    SEVERE_HTN,
)
from .base_eligibility_part_three import BaseEligibilityPartThree


class EligibilityPartThreePhaseThree(BaseEligibilityPartThree):
    def __init__(self, **kwargs):
        self.inclusion_a = TBD
        self.inclusion_b = TBD
        self.severe_htn = None
        super().__init__(**kwargs)

    def assess_eligibility(self: Any) -> None:
        """Subject is eligible if either a qualifying FBG (pre-diabetes)
        OR a qualifying OGTT

        However, OGTT overrides FBG. For example, a qualifying FBG
        that suggest pre-diabetes cannot override an OGTT that
        implies diabetes.

        FBG-HI + OGTT-HI -> NO
        FBG-HI + OGTT-PRE -> YES
        FBG-HI + OGTT-NORMAL -> NO

        FBG-PRE + OGTT-HI -> NO
        FBG-PRE + OGTT-PRE -> YES
        FBG-PRE + OGTT-NORMAL -> YES **(note FBG overrides
                                        OGTT in this case)

        FBG-NORMAL + OGTT-HI -> NO
        FBG-NORMAL + OGTT-PRE -> YES
        FBG-NORMAL + OGTT-NORMAL -> NO
        """
        # TODO: check if calculates correctly if glucose is HIGH 9999.99
        super().assess_eligibility()
        if (
            self.repeat_glucose_performed == PENDING
            or not self.fbg_category
            or not self.ogtt_category
        ):
            self.eligible = TBD
            self.reasons_ineligible.update(fbg_ogtt_incomplete=FBG_OGTT_INCOMPLETE)
        else:
            if self.ogtt_category == PRE_DM:
                self.eligible = YES
            elif self.ogtt_category == DM:
                self.eligible = NO
                self.reasons_ineligible.update(hi_ogtt=HI_OGTT)
            elif self.fbg_category == PRE_DM and self.ogtt_category == NORMAL:
                self.eligible = YES
            elif self.fbg_category == NORMAL and self.ogtt_category == NORMAL:
                self.eligible = NO
                self.reasons_ineligible.update(normal_fbg_ogtt=NORMAL_FBG_OGTT)
            elif self.fbg_category == DM and self.ogtt_category == NORMAL:
                self.eligible = NO
                self.reasons_ineligible.update(hi_fbg=HI_FBG)
        if self.calculated_egfr_value and self.calculated_egfr_value < 45.0:
            self.reasons_ineligible.update(egfr_low=EGFR_LT_45)
            self.eligible = NO

    def set_fld_attrs_on_model(self: Any) -> None:
        """Set extra attr on the model"""
        super().set_fld_attrs_on_model()
        self.model_obj.inclusion_a = self.inclusion_a
        self.model_obj.inclusion_b = self.inclusion_b
        self.model_obj.inclusion_c = NOT_APPLICABLE
        self.model_obj.inclusion_d = NOT_APPLICABLE

    def get_required_fields(self: Any) -> dict[str, FC]:
        """Get default fields as well as severe_htn"""
        fields = super().get_required_fields()
        fields.update({"severe_htn": FC(NO, SEVERE_HTN)})
        return fields

    @property
    def fbg_category(self):
        # FBG (6.1 to 6.9 mmol/L)
        value = (
            self.converted_fbg2_value
            if self.repeat_glucose_opinion == YES
            else self.converted_fbg_value
        )
        if not value:
            fbg_category = None
        elif 6.1 <= value < 7.0:
            fbg_category = PRE_DM
        elif value >= 7.0:
            fbg_category = DM
        elif value < 6.1:
            fbg_category = NORMAL
        else:
            raise ValueError("Invalid FBG value")
        return fbg_category

    @property
    def ogtt_category(self):
        # OGTT (7.8 to 11.10 mmol/L)
        value = (
            self.converted_ogtt2_value
            if self.repeat_glucose_opinion == YES
            else self.converted_ogtt_value
        )
        if not value:
            ogtt_category = None
        elif 7.8 <= value < 11.1:
            ogtt_category = PRE_DM
        elif value >= 11.1:
            ogtt_category = DM
        elif value < 7.8:
            ogtt_category = NORMAL
        else:
            raise ValueError("Invalid OGTT value")
        return ogtt_category
