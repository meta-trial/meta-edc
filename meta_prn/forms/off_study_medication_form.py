from datetime import datetime

from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixins import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_offstudy.modelform_mixins import OffstudyNonCrfModelFormMixin
from edc_sites.forms import SiteModelFormMixin
from edc_visit_schedule.modelform_mixins import VisitScheduleNonCrfModelFormMixin

from ..models import OffStudyMedication


class OffScheduleFormValidator(FormValidator):
    pass


class OffStudyMedicationForm(
    ActionItemFormMixin,
    VisitScheduleNonCrfModelFormMixin,
    OffstudyNonCrfModelFormMixin,
    SiteModelFormMixin,
    FormValidatorMixin,
    BaseModelFormMixin,
    forms.ModelForm,
):

    form_validator_cls = OffScheduleFormValidator
    get_by_model_attr = "offstudymedication_model"
    report_datetime_field_attr = "report_datetime"

    @property
    def subject_identifier(self) -> str:
        return self.cleaned_data.get("subject_identifier") or self.instance.subject_identifier

    @property
    def report_datetime(self) -> datetime:
        return self.cleaned_data.get(self.report_datetime_field_attr) or getattr(
            self.instance, self.report_datetime_field_attr
        )

    class Meta:
        model = OffStudyMedication
        fields = "__all__"
        help_text = {"subject_identifier": "(read-only)", "action_identifier": "(read-only)"}
        widgets = {
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "action_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
