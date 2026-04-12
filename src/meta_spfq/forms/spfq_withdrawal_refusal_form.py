from clinicedc_constants import NO, NOT_APPLICABLE, YES
from django import forms
from edc_form_validators import FormValidator, FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_prn.modelform_mixins import PrnSingletonModelFormMixin

from ..models import SpfqForWithdrawal
from .modelform_mixins import SpfqRefusalFormMixin


class SpfqRefusalFormValidator(FormValidator):
    def clean(self):
        self.required_if(
            YES, field="contact_attempted", field_required="contact_attempts_count"
        )
        self.required_if(NO, field="contact_made", field_required="contact_attempts_explained")


class SpfqForWithdrawalRefusalForm(
    SpfqRefusalFormMixin,
    PrnSingletonModelFormMixin,
    BaseModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = SpfqRefusalFormValidator
    report_datetime_field_attr = "report_datetime"

    def clean(self):
        cleaned_data: dict | None = super().clean()
        self.check_registered_subject(cleaned_data)
        self.check_subject_consent(cleaned_data)
        if cleaned_data.get("contact_attempted") == NOT_APPLICABLE:
            raise forms.ValidationError("Invalid. Select YES or NO")
        return cleaned_data

    class Meta:
        model = SpfqForWithdrawal
        fields = "__all__"
        widgets = {  # noqa: RUF012
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
