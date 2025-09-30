from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_action_item.forms import ActionItemFormMixin
from edc_form_validators import FormValidatorMixin
from edc_registration.models import RegisteredSubject
from edc_sites.modelform_mixins import SiteModelFormMixin

from meta_consent.models import SubjectConsentSpfq
from meta_rando.models import SpfqList


class SubjectConsentSpfqForm(
    SiteModelFormMixin, ActionItemFormMixin, FormValidatorMixin, forms.ModelForm
):
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
                        "Subject not found .A subject with this identifier "
                        "has not been selected for the sub-study."
                    )
                }
            ) from e
        return cleaned_data

    class Meta:
        model = SubjectConsentSpfq
        fields = "__all__"
        widgets = {  # noqa: RUF012
            "action_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
