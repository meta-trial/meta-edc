from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..form_validators import GlucoseOgttFormValidator
from ..models import GlucoseOgtt


class GlucoseOgttForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = GlucoseOgttFormValidator

    class Meta:
        model = GlucoseOgtt
        fields = "__all__"
