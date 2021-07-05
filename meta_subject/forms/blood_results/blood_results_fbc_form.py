from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin

from meta_form_validators.form_validators import BloodResultsFbcFormValidator

from ...models import BloodResultsFbc


class BloodResultsFbcForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsFbcFormValidator

    class Meta:
        model = BloodResultsFbc
        fields = "__all__"
