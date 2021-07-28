from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import ComplicationsGlycemia


class AdditionalScreeningFormValidator(FormValidator):
    def clean(self):
        pass


class ComplicationsGlycemiaForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = AdditionalScreeningFormValidator

    class Meta:
        model = ComplicationsGlycemia
        fields = "__all__"
