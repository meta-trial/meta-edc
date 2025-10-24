from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..form_validators import GlucoseFbgFormValidator
from ..models import GlucoseFbg


class GlucoseFbgForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = GlucoseFbgFormValidator

    class Meta:
        model = GlucoseFbg
        fields = "__all__"
