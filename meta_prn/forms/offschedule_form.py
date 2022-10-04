from django import forms
from edc_action_item.forms.action_item_form_mixin import ActionItemFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_form_validators.form_validator_mixins import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_prn.modelform_mixins import PrnFormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from edc_visit_schedule.modelform_mixins import OffScheduleModelFormMixin

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

    class Meta:
        model = OffSchedule
        fields = "__all__"
