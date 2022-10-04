from __future__ import annotations

from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_form_validators import INVALID_ERROR
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixins import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_offstudy.modelform_mixins import OffstudyNonCrfModelFormMixin
from edc_prn.modelform_mixins import PrnFormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from edc_utils.date import to_local
from edc_visit_schedule.modelform_mixins import VisitScheduleNonCrfModelFormMixin

from ..models import OffStudyMedication


class OffStudyMedicationFormValidator(PrnFormValidatorMixin, FormValidator):
    def clean(self):
        if (
            self.cleaned_data.get("stop_date")
            and self.report_datetime
            and self.cleaned_data.get("stop_date") > to_local(self.report_datetime).date()
        ):
            self.raise_validation_error(
                {"stop_date": "Cannot be after report date."}, INVALID_ERROR
            )
        if (
            self.cleaned_data.get("last_dose_date")
            and self.cleaned_data.get("stop_date")
            and self.cleaned_data.get("last_dose_date") > self.cleaned_data.get("stop_date")
        ):
            self.raise_validation_error(
                {"last_dose_date": "Cannot be after decision to stop medication."},
                INVALID_ERROR,
            )
        self.validate_other_specify(field="reason", other_specify_field="reason_other")


class OffStudyMedicationForm(
    ActionItemFormMixin,
    VisitScheduleNonCrfModelFormMixin,
    OffstudyNonCrfModelFormMixin,
    SiteModelFormMixin,
    BaseModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):

    form_validator_cls = OffStudyMedicationFormValidator
    get_by_model_attr = "offstudymedication_model"

    class Meta:
        model = OffStudyMedication
        fields = "__all__"
        help_text = {"subject_identifier": "(read-only)", "action_identifier": "(read-only)"}
        widgets = {
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "action_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
