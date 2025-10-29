from clinicedc_constants import NO, YES
from django import forms
from edc_form_validators import FormValidator, FormValidatorMixin
from edc_glucose.form_validators import OgttFormValidatorMixin
from edc_glucose.utils import validate_glucose_as_millimoles_per_liter

from ..models import MissingOgttNote


class MissingOgttNoteFormValidator(OgttFormValidatorMixin, FormValidator):
    def clean(self):
        self.applicable_if(YES, field="result_status", field_applicable="fasting")
        self.required_if(YES, NO, field="fasting", field_required="ogtt_base_datetime")
        self.required_if(YES, NO, field="fasting", field_required="ogtt_datetime")
        self.required_if(YES, NO, field="fasting", field_required="ogtt_value")
        self.applicable_if(YES, NO, field="fasting", field_applicable="ogtt_units")
        validate_glucose_as_millimoles_per_liter("ogtt", self.cleaned_data)
        self.validate_ogtt_dates()
        self.validate_ogtt_time_interval()


class MissingOgttNoteForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = MissingOgttNoteFormValidator

    class Meta:
        model = MissingOgttNote
        fields = "__all__"
        help_text = {"subject_identifier": "(read-only)", "name": "(read-only)"}  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "report_model": forms.TextInput(attrs={"readonly": "readonly"}),
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
