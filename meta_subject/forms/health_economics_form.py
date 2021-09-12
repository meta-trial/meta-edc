from django import forms
from edc_crf.forms import CrfFormValidatorMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_he.form_validators import HeEducationFormValidatorMixin

from ..models import HealthEconomics


class HealthEconomicsFormValidator(
    CrfFormValidatorMixin, HeEducationFormValidatorMixin, FormValidator
):
    def clean(self):
        self.clean_education()


class HealthEconomicsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsFormValidator

    class Meta:
        model = HealthEconomics
        fields = "__all__"
