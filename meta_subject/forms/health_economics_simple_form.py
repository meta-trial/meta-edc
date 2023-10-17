from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_he.form_validators import SimpleFormValidatorMixin

from ..models import HealthEconomicsSimple


class HealthEconomicsFormValidator(SimpleFormValidatorMixin, CrfFormValidator):
    def clean(self):
        self.clean_education()


class HealthEconomicsSimpleForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsFormValidator

    class Meta:
        model = HealthEconomicsSimple
        fields = "__all__"
