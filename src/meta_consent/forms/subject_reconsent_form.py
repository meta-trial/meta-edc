from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_action_item.forms import ActionItemFormMixin
from edc_form_validators import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_registration.models import RegisteredSubject
from edc_sites.forms import SiteModelFormMixin

from ..models import SubjectReconsent


class SubjectReconsentForm(
    SiteModelFormMixin,
    ActionItemFormMixin,
    BaseModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    def clean(self):
        cleaned_data = super().clean()
        try:
            RegisteredSubject.objects.get(
                subject_identifier=cleaned_data.get("subject_identifier"),
                identity=cleaned_data.get("identity"),
            )
        except ObjectDoesNotExist as e:
            raise forms.ValidationError({"identity": "Identity number does not match."}) from e
        return cleaned_data

    class Meta:
        model = SubjectReconsent
        fields = "__all__"
        help_text = {"action_identifier": "(read-only)", "subject_identifier": "(read-only)"}  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "action_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
