from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import AdditionalScreening


class AdditionalScreeningFormValidator(FormValidator):
    def clean(self):
        pass


class AdditionalScreeningForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = AdditionalScreeningFormValidator

    class Meta:
        model = AdditionalScreening
        fields = "__all__"
