from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_screening.fc import FC
from edc_screening.screening_eligibility import ScreeningEligibility


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
        return {
            "acute_condition": FC(NO, "Acute condition"),
            "acute_metabolic_acidosis": FC(NO, "Acute metabolic acidosis"),
            "advised_to_fast": FC([YES, NOT_APPLICABLE], "Not advised to fast"),
            "alcoholism": FC(NO, "Alcoholism"),
            "congestive_heart_failure": FC(NO, "Congestive heart failure"),
            "liver_disease": FC(NO, "Liver disease"),
            "metformin_sensitivity": FC(NO, "Metformin sensitivity"),
            "renal_function_condition": FC(NO, "Renal function"),
            "tissue_hypoxia_condition": FC(NO, "Tissue hypoxia"),
            "appt_datetime": FC(ignore_if_missing=True),
            "has_dm": FC(NO, "Diabetes"),
            "on_dm_medication": FC(NO, "taking anti-diabetic medications"),
        }

    def set_eligible_model_field(self):
        setattr(self.model_obj, self.eligible_fld_name, self.eligible)
