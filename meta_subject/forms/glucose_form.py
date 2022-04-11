from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import FbgOgttFormValidatorMixin

from ..models import Glucose


class GlucoseFormValidator(FbgOgttFormValidatorMixin, FormValidator):
    def clean(self):
        self.validate_glucose_testing_matrix()


class GlucoseForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = GlucoseFormValidator

    class Meta:
        model = Glucose  # "Glucose (IFG, OGTT)"
        fields = "__all__"
