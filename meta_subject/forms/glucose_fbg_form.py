from decimal import Decimal

from django import forms
from edc_constants.constants import NO, YES
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import INVALID_ERROR
from edc_glucose.utils import validate_glucose_as_millimoles_per_liter

from ..models import GlucoseFbg


class GlucoseFbgFormValidator(CrfFormValidator):
    def clean(self):
        converted_value = None
        self.required_if(YES, field="fasting", field_required="fasting_duration_str")
        self.required_if(NO, field="fbg_performed", field_required="fbg_not_performed_reason")
        self.required_if(YES, field="fbg_performed", field_required="fbg_datetime")
        if self.cleaned_data.get("fbg_datetime") and self.cleaned_data.get(
            "fbg_datetime"
        ) < self.cleaned_data.get("report_datetime"):
            self.raise_validation_error(
                {"fbg_datetime": "Invalid. Must be on or after report date above"},
                INVALID_ERROR,
            )
        self.required_if(YES, field="fbg_performed", field_required="fbg_value")
        if self.cleaned_data.get("fbg_value") is not None:
            converted_value = validate_glucose_as_millimoles_per_liter(
                "fbg", self.cleaned_data
            )

        self.applicable_if(YES, field="fbg_performed", field_applicable="fbg_units")

        # repeat_fbg_date
        condition = converted_value and converted_value >= Decimal("7.0")
        self.required_if_true(condition, field_required="repeat_fbg_date")
        if self.cleaned_data.get("repeat_fbg_date") and self.cleaned_data.get("fbg_datetime"):
            diffdays = (
                self.cleaned_data.get("repeat_fbg_date")
                - self.cleaned_data.get("fbg_datetime").date()
            ).days
            if not (7 <= diffdays <= 10):
                self.raise_validation_error(
                    {
                        "repeat_fbg_date": (
                            f"Must be 7 to 10 days from date measured above. Got {diffdays}."
                        )
                    },
                    INVALID_ERROR,
                )


class GlucoseFbgForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = GlucoseFbgFormValidator

    class Meta:
        model = GlucoseFbg
        fields = "__all__"
