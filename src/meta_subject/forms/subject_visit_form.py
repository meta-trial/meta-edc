from django import forms
from edc_consent.modelform_mixins import RequiresConsentModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_offstudy.modelform_mixins import OffstudyNonCrfModelFormMixin
from edc_visit_tracking.form_validators import VisitFormValidator
from edc_visit_tracking.modelform_mixins import VisitTrackingModelFormMixin

from meta_prn.models import OffStudyMedication
from meta_visit_schedule.constants import SCHEDULE_DM_REFERRAL

from ..models import SubjectVisit


class SubjectVisitFormValidator(VisitFormValidator):
    validate_missed_visit_reason = False


class SubjectVisitForm(
    RequiresConsentModelFormMixin,
    VisitTrackingModelFormMixin,
    OffstudyNonCrfModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = SubjectVisitFormValidator

    def clean(self):
        cleaned_data = super().clean()
        if (
            self.cleaned_data.get("appointment").schedule_name == SCHEDULE_DM_REFERRAL
            and not OffStudyMedication.objects.filter(
                subject_identifier=self.subject_identifier
            ).exists()
        ):
            raise forms.ValidationError(
                f"Submit form `{OffStudyMedication._meta.verbose_name}` first."
            )
        return cleaned_data

    class Meta:
        model = SubjectVisit
        fields = "__all__"
