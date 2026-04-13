from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.modelform_mixins import SiteModelFormMixin

from ..models import SpfqForWithdrawalList, SubjectConsentSpfqForWithdrawal
from .modelform_mixins import SubjectConsentSpfqFormMixin


class SubjectConsentSpfqForWithdrawalForm(
    SubjectConsentSpfqFormMixin,
    SiteModelFormMixin,
    ActionItemFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    list_model_cls = SpfqForWithdrawalList
    error_msg = (
        "Subject not found .A subject with this identifier "
        "has not been selected for the SPFQ for withdrawals sub-study."
    )

    class Meta:
        model = SubjectConsentSpfqForWithdrawal
        fields = "__all__"
        # widgets = {
        #     "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        # }
