from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_microscopy.form_validators import MalariaTestFormValidator

from ..models import MalariaTest


class MalariaTestForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = MalariaTestFormValidator

    class Meta:
        model = MalariaTest
        fields = "__all__"
