from django import forms
from edc_adverse_event.modelform_mixins import AeModelFormMixin
from edc_adverse_event.utils import validate_ae_initial_outcome_date
from edc_form_validators import FormValidator, FormValidatorMixin


class AeReviewFormValidator(FormValidator):
    def clean(self):
        pass


class AeReviewModelFormMixin(
    AeModelFormMixin,
    FormValidatorMixin,
):
    form_validator_cls = AeReviewFormValidator

    def clean(self):
        cleaned_data = super().clean()
        validate_ae_initial_outcome_date(self)
        return cleaned_data

    class Meta:
        help_text = {"subject_identifier": "(read-only)", "action_identifier": "(read-only)"}  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "action_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
