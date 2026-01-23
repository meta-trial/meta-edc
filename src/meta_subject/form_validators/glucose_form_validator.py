from clinicedc_constants import PENDING, YES
from edc_crf.crf_form_validator import CrfFormValidator
from edc_glucose.form_validators import FbgOgttFormValidatorMixin

from ..constants import AMENDMENT_DATE
from .mixins import EndpointValidatorMixin, RepeatFbgDateValidatorMixin


class GlucoseFormValidator(
    EndpointValidatorMixin,
    RepeatFbgDateValidatorMixin,
    FbgOgttFormValidatorMixin,
    CrfFormValidator,
):
    def clean(self):
        self.required_if(YES, field="fasting", field_required="fasting_duration_str")
        self.validate_glucose_testing_matrix(include_fbg=True)
        has_results = (
            self.cleaned_data.get("fbg_value") is not None
            and self.cleaned_data.get("ogtt_value") is not None
            and self.cleaned_data.get("report_datetime").date() >= AMENDMENT_DATE
        )
        self.applicable_if_true(has_results, field_applicable="endpoint_today")
        if has_results:
            self.validate_endpoint_fields(
                performed=bool(
                    self.cleaned_data.get("fbg_value") is not None
                    or self.cleaned_data.get("ogtt_value") is not None
                )
            )
        self.required_if(PENDING, field="endpoint_today", field_required="repeat_fbg_date")
        self.validate_repeat_fbg_date()
