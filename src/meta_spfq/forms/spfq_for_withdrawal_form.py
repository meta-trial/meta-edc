from django import forms
from edc_form_validators import FormValidatorMixin
from edc_prn.modelform_mixins import PrnSingletonModelFormMixin

from ..models import SpfqForWithdrawal


class SpfqForWithdrawalForm(PrnSingletonModelFormMixin, FormValidatorMixin, forms.ModelForm):
    report_datetime_field_attr = "report_datetime"

    def get_subject_identifier(self):
        if not self.cleaned_data.get("registered_subject"):
            raise forms.ValidationError("Registered subject may not be None")
        return self.cleaned_data.get("registered_subject").subject_identifier

    class Meta:
        model = SpfqForWithdrawal
        fields = "__all__"
