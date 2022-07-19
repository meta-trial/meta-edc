from django import forms
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixin import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from ..models import OffstudyMedication


class OffScheduleFormValidator(FormValidator):
    pass


class OffstudyMedicationForm(
    SiteModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):

    form_validator_cls = OffScheduleFormValidator

    class Meta:
        model = OffstudyMedication
        fields = "__all__"
        help_text = {"subject_identifier": "(read-only)", "action_identifier": "(read-only)"}
        widgets = {
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "action_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
