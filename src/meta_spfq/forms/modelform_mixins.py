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


class SubjectConsentSpfqFormMixin:
    list_model_cls = SpfqList
    error_msg = (
        "Subject not found .A subject with this identifier "
        "has not been selected for the SPFQ sub-study."
    )

    def clean(self):
        cleaned_data = super().clean()
        try:
            RegisteredSubject.objects.get(
                subject_identifier=cleaned_data.get("subject_identifier"),
                initials=cleaned_data.get("initials"),
                gender=cleaned_data.get("gender"),
            )
        except ObjectDoesNotExist as e:
            try:
                rs_obj = RegisteredSubject.objects.get(
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
            else:
                raise forms.ValidationError(
                    "Subject known to the META trial but gender/initials do not match. "
                    f"Expected gender={rs_obj.gender}, initials={rs_obj.initials}. "
                    "Is this the correct subject?"
                ) from e
        self.check_if_subject_on_list(cleaned_data)

        return cleaned_data

    def check_if_subject_on_list(self, cleaned_data: dict):
        try:
            self.list_model_cls.objects.get(
                subject_identifier=cleaned_data.get("subject_identifier"),
            )
        except ObjectDoesNotExist as e:
            raise forms.ValidationError({"__all__": self.error_msg}) from e
