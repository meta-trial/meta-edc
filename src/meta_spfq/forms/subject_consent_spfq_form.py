from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.modelform_mixins import SiteModelFormMixin

from ..models import SubjectConsentSpfq
from .modelform_mixins import SubjectConsentSpfqFormMixin


class SubjectConsentSpfqForm(
    SubjectConsentSpfqFormMixin,
    SiteModelFormMixin,
    ActionItemFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    class Meta:
        model = SubjectConsentSpfq
        fields = "__all__"
        widgets = {  # noqa: RUF012
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
