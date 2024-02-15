from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import INVALID_ERROR
from edc_glucose.utils import validate_glucose_as_millimoles_per_liter
from edc_lab_results.form_validator_mixins import (
    BloodResultsFormValidatorMixin,
    BloodResultsGluFormValidatorMixin,
)

from ..models import GlucoseFbg


class GlucoseFbgFormValidator(
    BloodResultsGluFormValidatorMixin, BloodResultsFormValidatorMixin, CrfFormValidator
):
    def clean(self):
        if (
            self.cleaned_data.get("report_datetime")
            and self.cleaned_data.get("assay_datetime")
            and self.cleaned_data.get("assay_datetime")
            < self.cleaned_data.get("report_datetime")
        ):
            self.raise_validation_error(
                {"assay_datetime": "Cannot be before report date"}, INVALID_ERROR
            )
        if self.cleaned_data.get("glucose_value") is not None:
            validate_glucose_as_millimoles_per_liter("glucose", self.cleaned_data)


class GlucoseFbgForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = GlucoseFbgFormValidator

    class Meta:
        model = GlucoseFbg
        fields = "__all__"
