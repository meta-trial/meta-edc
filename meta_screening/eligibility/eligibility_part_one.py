from edc_constants.constants import FEMALE, MALE, NO, NOT_APPLICABLE, YES
from edc_screening.screening_eligibility import FC, ScreeningEligibility

from meta_edc.meta_version import PHASE_THREE, get_meta_version


class EligibilityPartOne(ScreeningEligibility):

    eligible_fld_name = "eligible_part_one"
    reasons_ineligible_fld_name = "reasons_ineligible_part_one"

    def __init__(self, **kwargs):
        self.age_in_years = None
        self.art_six_months = None
        self.gender = None
        self.hiv_pos = None
        self.lives_nearby = None
        self.meta_phase_two = None
        self.on_rx_stable = None
        self.pregnant = None
        self.staying_nearby_6 = None
        self.staying_nearby_12 = None
        super().__init__(**kwargs)

    def get_required_fields(self) -> dict[str, FC]:
        if get_meta_version() == PHASE_THREE:
            fields = {
                "age_in_years": FC(range(18, 120), "age<18"),
                "art_six_months": FC(YES, "ART<6m"),
                "gender": FC([MALE, FEMALE], "gender invalid"),
                "hiv_pos": FC(YES, "not HIV+"),
                "lives_nearby": FC(YES, "Not living nearby"),
                "meta_phase_two": FC(NO, "META Phase 2 participant"),
                "on_rx_stable": FC(YES, "ART not stable"),
                "pregnant": FC([NO, NOT_APPLICABLE], "Pregnant (unconfirmed)"),
                "staying_nearby_12": FC(YES, "Unable/Unwilling to stay nearby for 12m"),
            }
        else:
            fields = {
                "age_in_years": FC(range(18, 120), "age<18"),
                "art_six_months": FC(YES, "ART<6m"),
                "gender": FC([MALE, FEMALE], "gender invalid"),
                "hiv_pos": FC(YES, "not HIV+"),
                "lives_nearby": FC(YES, "Not living nearby"),
                "on_rx_stable": FC(YES, "ART not stable"),
                "pregnant": FC([NO, NOT_APPLICABLE], "Pregnant (unconfirmed)"),
                "staying_nearby_6": FC(YES, "Unable/Unwilling to stay nearby for 6m"),
            }
        return fields

    def set_fld_attrs_on_model(self) -> None:
        if self.eligible == YES:
            self.model_obj.continue_part_two = YES
        else:
            self.model_obj.continue_part_two = NO
