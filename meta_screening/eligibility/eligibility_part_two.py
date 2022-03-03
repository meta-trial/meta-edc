from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_screening.screening_eligibility import FC, ScreeningEligibility

from meta_edc.meta_version import PHASE_THREE, get_meta_version


class EligibilityPartTwo(ScreeningEligibility):

    eligible_fld_name = "eligible_part_two"
    reasons_ineligible_fld_name = "reasons_ineligible_part_two"

    def __init__(self, **kwargs):
        self.acute_condition = None
        self.acute_metabolic_acidosis = None
        self.advised_to_fast = None
        self.alcoholism = None
        self.appt_datetime = None
        self.congestive_heart_failure = None
        self.has_dm = None
        self.on_dm_medication = None
        self.liver_disease = None
        self.metformin_sensitivity = None
        self.renal_function_condition = None
        self.tissue_hypoxia_condition = None
        super().__init__(**kwargs)

    def get_required_fields(self) -> dict[str, FC]:
        fields = {
            "acute_condition": FC(NO, None),
            "acute_metabolic_acidosis": FC(NO, None),
            "advised_to_fast": FC([YES, NOT_APPLICABLE], "Not advised to fast"),
            "alcoholism": FC(NO, None),
            "congestive_heart_failure": FC(NO, None),
            "liver_disease": FC(NO, None),
            "metformin_sensitivity": FC(NO, None),
            "renal_function_condition": FC(NO, None),
            "tissue_hypoxia_condition": FC(NO, None),
            "appt_datetime": FC(ignore_if_missing=True),
        }
        if get_meta_version() == PHASE_THREE:
            fields.update(
                {
                    "has_dm": FC(NO, "Diabetic"),
                    "on_dm_medication": FC(NO, "taking anti-diabetic medications"),
                }
            )
        return fields

    def set_eligible_model_field(self):
        setattr(self.model_obj, self.eligible_fld_name, self.eligible)
