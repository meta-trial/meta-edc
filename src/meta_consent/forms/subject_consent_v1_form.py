from django import forms
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from ..form_validators import SubjectConsentFormValidator
from ..models import SubjectConsentV1
from .subject_consent_form import help_texts, widgets


class SubjectConsentV1Form(
    SiteModelFormMixin, ConsentModelFormMixin, FormValidatorMixin, forms.ModelForm
):
    form_validator_cls = SubjectConsentFormValidator

    def validate_gender_of_consent(self):
        return None

    def validate_guardian_and_dob(self):
        return None

    class Meta:
        model = SubjectConsentV1
        fields = "__all__"
        help_texts = help_texts
        widgets = widgets
