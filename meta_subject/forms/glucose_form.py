from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..form_validators import GlucoseFormValidator
from ..models import Glucose


class GlucoseForm(CrfModelFormMixin, ActionItemCrfFormMixin, forms.ModelForm):
    form_validator_cls = GlucoseFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = Glucose
        fields = "__all__"
