from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_registration.models import RegisteredSubject

from ..models import SpfqList, SubjectConsentSpfq


class SpfqRefusalFormMixin:
    @staticmethod
    def check_registered_subject(cleaned_data: dict | None):
        if cleaned_data:
            try:
                RegisteredSubject.objects.get(
                    subject_identifier=cleaned_data.get("subject_identifier")
                )
            except ObjectDoesNotExist as e:
                raise forms.ValidationError(
                    {
                        "__all__": (
                            "Subject not known to the META trial. "
                            "Check that the identifier, initials and gender match the patient "
                            "register from the main META trial."
                        )
                    }
                ) from e

    @staticmethod
    def check_spfq_list(cleaned_data: dict | None):
        if cleaned_data:
            try:
                SpfqList.objects.get(
                    subject_identifier=cleaned_data.get("subject_identifier"),
                )
            except ObjectDoesNotExist as e:
                raise forms.ValidationError(
                    {
                        "__all__": (
                            "Subject not found. A subject with this identifier "
                            "has not been selected for the sub-study."
                        )
                    }
                ) from e

    @staticmethod
    def check_subject_consent(cleaned_data: dict | None):
        try:
            SubjectConsentSpfq.objects.get(
                subject_identifier=cleaned_data.get("subject_identifier"),
            )
        except ObjectDoesNotExist:
            pass
        else:
            raise forms.ValidationError(
                {"__all__": "Subject has already consented for the sub-study."}
            )
