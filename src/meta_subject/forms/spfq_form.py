from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_registration.models import RegisteredSubject

from meta_consent.models import SubjectConsentSpfq
from meta_rando.models import SpfqList

from ..models import Spfq


class SpfqFormValidator(CrfFormValidator):
    pass


class SpfqForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = SpfqFormValidator

    def clean(self):
        cleaned_data = super().clean()

        try:
            RegisteredSubject.objects.get(
                subject_identifier=cleaned_data.get("subject_identifier"),
                initials=cleaned_data.get("initials"),
                gender=cleaned_data.get("gender"),
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

        try:
            SubjectConsentSpfq.objects.get(
                subject_identifier=cleaned_data.get("subject_identifier"),
            )
        except ObjectDoesNotExist as e:
            raise forms.ValidationError(
                {"__all__": "Subject not consented for the sub-study."}
            ) from e
        return cleaned_data

    class Meta:
        model = Spfq
        fields = "__all__"
