from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_action_item.forms import ActionItemFormMixin
from meta_form_validators.form_validators import BloodResultsRftFormValidator

from ...models import BloodResultsRft


class BloodResultsRftForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsRftFormValidator

    class Meta:
        model = BloodResultsRft
        fields = "__all__"
