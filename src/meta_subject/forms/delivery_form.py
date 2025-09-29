from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..form_validators import DeliveryFormValidator
from ..models import Delivery


class DeliveryForm(CrfModelFormMixin, ActionItemCrfFormMixin, forms.ModelForm):
    report_datetime_allowance = 364

    form_validator_cls = DeliveryFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = Delivery
        fields = "__all__"
