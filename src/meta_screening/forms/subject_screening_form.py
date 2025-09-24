from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin

from ..form_validators import SubjectScreeningFormValidator
from ..models import SubjectScreening


class SubjectScreeningForm(
    AlreadyConsentedFormMixin, SiteModelFormMixin, FormValidatorMixin, forms.ModelForm
):
    form_validator_cls = SubjectScreeningFormValidator

    class Meta:
        model = SubjectScreening
        fields = "__all__"
