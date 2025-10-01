from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_crf.crf_form_validator import CrfFormValidator
from edc_form_validators import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_prn.modelform_mixins import PrnSingletonModelFormMixin
from edc_registration.models import RegisteredSubject

from ..models import Spfq, SpfqList, SubjectConsentSpfq


class SpfqFormValidator(CrfFormValidator):
    pass


class SpfqForm(
    PrnSingletonModelFormMixin, BaseModelFormMixin, FormValidatorMixin, forms.ModelForm
):
    form_validator_cls = SpfqFormValidator
    report_datetime_field_attr = "report_datetime"

    def clean(self):
        cleaned_data = super().clean()

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
        widgets = {  # noqa: RUF012
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
