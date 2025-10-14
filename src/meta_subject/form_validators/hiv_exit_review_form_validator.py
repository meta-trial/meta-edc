from edc_constants.constants import OTHER
from edc_crf.crf_form_validator import CrfFormValidator


class HivExitReviewFormValidator(CrfFormValidator):
    def clean(self):
        self.required_if_not_none(
            "viral_load", "viral_load_date", field_required_evaluate_as_int=True
        )

        self.required_if_not_none("cd4", "cd4_date", field_required_evaluate_as_int=True)

        self.required_if(
            OTHER,
            field="current_arv_regimen",
            field_required="other_current_arv_regimen",
        )
