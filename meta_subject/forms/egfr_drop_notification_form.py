from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..form_validators import EgfrDropNotificationFormValidator
from ..models import EgfrDropNotification


class EgfrDropNotificationForm(CrfModelFormMixin, ActionItemCrfFormMixin, forms.ModelForm):
    form_validator_cls = EgfrDropNotificationFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = EgfrDropNotification
        fields = "__all__"
