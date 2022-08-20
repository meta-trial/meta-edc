from django import forms
from edc_form_validators import FormValidatorMixin
from edc_refusal.forms import ScreeningFormMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin

from ..form_validators import SubjectRefusalFormValidator
from ..models import SubjectRefusal


class SubjectRefusalForm(
    AlreadyConsentedFormMixin, ScreeningFormMixin, FormValidatorMixin, forms.ModelForm
):

    form_validator_cls = SubjectRefusalFormValidator

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = SubjectRefusal
        fields = "__all__"
