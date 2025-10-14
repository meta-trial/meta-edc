from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_action_item.forms.action_item_form_mixin import ActionItemFormMixin
from edc_appointment.constants import MISSED_APPT
from edc_appointment.models import Appointment
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixins import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_prn.modelform_mixins import PrnFormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from edc_visit_schedule.modelform_mixins import OffScheduleModelFormMixin

from meta_subject.models import HivExitReview

from ..models import OffSchedule


class OffScheduleFormValidator(PrnFormValidatorMixin, FormValidator):
    pass


class OffScheduleForm(
    OffScheduleModelFormMixin,
    SiteModelFormMixin,
    ActionItemFormMixin,
    BaseModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = OffScheduleFormValidator
    report_datetime_field_attr = "offschedule_datetime"

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    def clean(self):
        try:
            HivExitReview.objects.get(
                subject_visit__subject_identifier=self.get_subject_identifier()
            )
        except ObjectDoesNotExist as e:
            # if last visit was missed do not require
            last_appointment = (
                Appointment.objects.filter(
                    subject_identifier=self.get_subject_identifier(),
                    subjectvisit__isnull=False,
                )
                .order_by("appt_datetime")
                .last()
            )
            if last_appointment.appt_timing != MISSED_APPT:
                raise forms.ValidationError(
                    "Hiv Exit Review CRF is required before taking subject off schedule."
                ) from e

    class Meta:
        model = OffSchedule
        fields = "__all__"
