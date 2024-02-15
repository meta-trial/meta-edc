from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import FollowupVitals


class FollowupVitalsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = CrfFormValidator

    class Meta:
        model = FollowupVitals
        fields = "__all__"
