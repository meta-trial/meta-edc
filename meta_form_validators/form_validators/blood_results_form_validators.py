from django import forms
from edc_blood_results import BloodResultsFormValidatorMixin
from edc_constants.constants import FASTING, YES
from edc_form_validators.form_validator import FormValidator
from edc_glucose.utils import validate_glucose_as_millimoles_per_liter
from edc_lab_panel.panels import (
    blood_glucose_panel,
    blood_glucose_poc_panel,
    fbc_panel,
    hba1c_panel,
    hba1c_poc_panel,
    insulin_panel,
    lft_panel,
    lipids_panel,
    rft_panel,
)
from edc_reportable import BmiFormValidatorMixin

from meta_labs.lab_profiles import chemistry_panel


class BaseBloodResultsGluFormValidator:
    @property
    def reportables_evaluator_options(self):
        if not self.cleaned_data.get("fasting"):
            raise forms.ValidationError({"fasting": "This field is required."})
        fasting = (
            True
            if (
                (self.cleaned_data.get("fasting") == FASTING)
                or (self.cleaned_data.get("fasting") == YES)
            )
            else False
        )
        return dict(fasting=fasting)

    def evaluate_value(self, field_name):
        if field_name == "glucose_value":
            validate_glucose_as_millimoles_per_liter("glucose", self.cleaned_data)


class BloodResultsGluFormValidator(
    BaseBloodResultsGluFormValidator, BloodResultsFormValidatorMixin, FormValidator
):
    panel = blood_glucose_panel


class BloodResultsGluPocFormValidator(
    BaseBloodResultsGluFormValidator, BloodResultsFormValidatorMixin, FormValidator
):
    panel = blood_glucose_poc_panel


class BloodResultsFbcFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panel = fbc_panel


class BloodResultsHba1cFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panel = hba1c_panel


class BloodResultsHba1cPocFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panel = hba1c_poc_panel


class BloodResultsLipidFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panels = [lipids_panel, chemistry_panel]


class BloodResultsLftFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panels = [lft_panel, chemistry_panel]


class BloodResultsRftFormValidator(
    BloodResultsFormValidatorMixin, BmiFormValidatorMixin, FormValidator
):
    panels = [rft_panel, chemistry_panel]

    def clean(self):
        super().clean()
        self.validate_bmi()


class BloodResultsInsFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panels = [insulin_panel]
