from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import ComplicationsGlycemia


class ComplicationsGlycemiaForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = CrfFormValidator

    class Meta:
        model = ComplicationsGlycemia
        fields = "__all__"
