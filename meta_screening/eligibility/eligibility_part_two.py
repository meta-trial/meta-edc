from edc_constants.constants import NO, TBD, YES

from meta_edc.meta_version import PHASE_THREE, get_meta_version

from .base_eligibility_part_x import BaseEligibilityPartX


class EligibilityPartTwo(BaseEligibilityPartX):
    def assess_eligibility(self):
        """Updates model instance fields `eligible_part_two`
        and `reasons_ineligible_part_two`.
        """
        self.obj.eligible_part_two = TBD
        self.obj.reasons_ineligible_part_two = None
        self.check_for_required_field_values()
        reasons_ineligible = self.get_reasons_ineligible()
        self.obj.reasons_ineligible_part_two = "|".join(reasons_ineligible)
        self.obj.eligible_part_two = NO if reasons_ineligible else YES

    @classmethod
    def get_required_fields(cls):
        fields = [
            "congestive_heart_failure",
            "liver_disease",
            "alcoholism",
            "acute_metabolic_acidosis",
            "renal_function_condition",
            "tissue_hypoxia_condition",
            "acute_condition",
            "metformin_sensitivity",
        ]
        if get_meta_version() == PHASE_THREE:
            fields.extend(["has_dm", "on_dm_medication"])
        return fields

    def get_reasons_ineligible(self):
        reasons_ineligible = []
        responses = {}
        for field in self.get_required_fields():
            responses.update({field: getattr(self.obj, field)})
        for k, v in responses.items():
            if v == YES:
                reasons_ineligible.append(k.title().replace("_", " "))
        if not reasons_ineligible and self.obj.advised_to_fast == NO:
            reasons_ineligible.append("Not advised to fast")
        if not reasons_ineligible and not self.obj.appt_datetime:
            reasons_ineligible.append("Not scheduled for stage 2")
        return reasons_ineligible
