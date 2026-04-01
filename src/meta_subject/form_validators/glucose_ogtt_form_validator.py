from decimal import Decimal

from clinicedc_constants import NO, YES
from edc_crf.crf_form_validator import CrfFormValidator
from edc_glucose.form_validators import FbgOgttFormValidatorMixin

from ..constants import AMENDMENT_DATE
from .mixins import EndpointValidatorMixin


class GlucoseOgttFormValidator(
    EndpointValidatorMixin,
    FbgOgttFormValidatorMixin,
    CrfFormValidator,
):
    def clean(self):
        self.required_if(YES, field="fasting", field_required="fasting_duration_str")
        self.validate_glucose_testing_matrix(include_fbg=False)
        has_results = (
            self.cleaned_data.get("ogtt_value") is not None
            and self.cleaned_data.get("report_datetime").date() >= AMENDMENT_DATE
        )
        self.applicable_if_true(has_results, field_applicable="endpoint_today")
        if has_results:
            self.validate_endpoint_fields(
                performed=bool(self.cleaned_data.get("ogtt_value") is not None)
            )

    def is_endpoint(self):
        return (
            YES
            if (
                self.cleaned_data.get("ogtt_value")
                and self.cleaned_data.get("ogtt_value") >= Decimal("11.1")
            )
            else NO
        )
