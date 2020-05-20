from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from meta_screening.form_validators import GlucoseFormValidatorMixin
from meta_screening.forms import validate_glucose_as_millimoles_per_liter

from ..models import Glucose


class GlucoseFormValidator(GlucoseFormValidatorMixin, FormValidator):
    def clean(self):
        self.validate_ifg()
        self.validate_ogtt()
        self.validate_ogtt_dates()
        self.validate_glucose_dates()


class GlucoseForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = GlucoseFormValidator

    def clean(self):
        cleaned_data = super().clean()
        validate_glucose_as_millimoles_per_liter(cleaned_data)
        return cleaned_data

    class Meta:
        model = Glucose
        fields = "__all__"
