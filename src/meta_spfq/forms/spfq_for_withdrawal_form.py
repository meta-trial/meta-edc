from clinicedc_constants import NO, YES
from django import forms
from edc_constants.choices import YES_NO_NA
from edc_form_validators import FormValidator, FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_prn.modelform_mixins import PrnSingletonModelFormMixin

from ..models import SpfqForWithdrawal


class SpfqForWithdrawalFormValidator(FormValidator):
    def clean(self):
        self.required_if(YES, field="agreed_to_consented", field_required="consent_datetine")
        self.applicable_if(
            YES, field="agreed_to_consented", field_applicable="consent_reviewed"
        )
        self.applicable_if(
            YES, field="agreed_to_consented", field_applicable="study_questions"
        )
        self.applicable_if(
            YES, field="agreed_to_consented", field_applicable="assessment_score"
        )
        self.applicable_if(
            YES, field="agreed_to_consented", field_applicable="consent_signature"
        )
        self.applicable_if(YES, field="agreed_to_consented", field_applicable="consent_copy")
        self.applicable_if(
            NO, field="agreed_to_consented", field_applicable="contact_attempted"
        )
        self.required_if(
            YES, field="contact_attempted", field_required="contact_attempts_count"
        )
        self.required_if(NO, field="contact_made", field_required="contact_attempts_explained")


class SpfqForWithdrawalForm(
    PrnSingletonModelFormMixin, BaseModelFormMixin, FormValidatorMixin, forms.ModelForm
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["consent_reviewed"].choices = YES_NO_NA
        self.fields["study_questions"].choices = YES_NO_NA
        self.fields["assessment_score"].choices = YES_NO_NA
        self.fields["consent_signature"].choices = YES_NO_NA
        self.fields["consent_copy"].choices = YES_NO_NA

    form_validator_cls = SpfqForWithdrawalFormValidator
    report_datetime_field_attr = "report_datetime"

    def clean_consent_reviewed(self):
        return self.cleaned_data["consent_reviewed"]

    def clean_study_questions(self):
        return self.cleaned_data["study_questions"]

    def clean_assessment_score(self):
        return self.cleaned_data["assessment_score"]

    def clean_consent_signature(self):
        return self.cleaned_data["consent_signature"]

    def clean_consent_copy(self):
        return self.cleaned_data["consent_copy"]

    class Meta:
        model = SpfqForWithdrawal
        fields = "__all__"
