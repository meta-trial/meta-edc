from edc_constants.constants import FEMALE, MALE, NO, TBD, YES

from meta_edc.meta_version import PHASE_THREE, get_meta_version

from .base_eligibility_part_x import BaseEligibilityPartX


class EligibilityPartOne(BaseEligibilityPartX):
    def assess_eligibility(self):
        """Updates model instance fields `eligible_part_one`
        and `reasons_ineligible_part_one`.
        """
        self.obj.eligible_part_one = TBD
        self.obj.reasons_ineligible_part_one = None
        self.check_for_required_field_values()
        reasons_ineligible = self.get_reasons_ineligible()
        self.obj.reasons_ineligible_part_one = "|".join(reasons_ineligible)
        self.obj.eligible_part_one = NO if reasons_ineligible else YES
        if self.obj.eligible_part_one == YES or self.obj.eligible_part_two != TBD:
            self.obj.continue_part_two = YES

    @classmethod
    def get_required_fields(cls):
        return [
            "gender",
            "age_in_years",
            "hiv_pos",
            "art_six_months",
            "on_rx_stable",
            "lives_nearby",
            (
                "staying_nearby_12"
                if get_meta_version() == PHASE_THREE
                else "staying_nearby_6"
            ),
            "pregnant",
        ]

    def get_reasons_ineligible(self):
        reasons_ineligible = []
        if self.obj.gender not in [MALE, FEMALE]:
            reasons_ineligible.append("gender invalid")
        if self.obj.age_in_years < 18:
            reasons_ineligible.append("age<18")
        if self.obj.hiv_pos == NO:
            reasons_ineligible.append("not HIV+")
        if self.obj.art_six_months == NO:
            reasons_ineligible.append("ART<6m")
        if self.obj.on_rx_stable == NO:
            reasons_ineligible.append("ART not stable")
        if self.obj.lives_nearby == NO:
            reasons_ineligible.append("Not living nearby")
        if get_meta_version() == PHASE_THREE and self.obj.staying_nearby_12 == NO:
            reasons_ineligible.append("Unable/Unwilling to stay nearby")
        elif self.obj.staying_nearby_6 == NO:
            reasons_ineligible.append("Unable/Unwilling to stay nearby")
        if self.obj.pregnant == YES:
            reasons_ineligible.append("Pregnant (unconfirmed)")
        return reasons_ineligible
