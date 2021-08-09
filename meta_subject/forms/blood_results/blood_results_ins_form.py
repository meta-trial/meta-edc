from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin

from meta_form_validators.form_validators import BloodResultsInsFormValidator

from ...models import BloodResultsIns


class BloodResultsInsForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsInsFormValidator

    class Meta:
        model = BloodResultsIns
        fields = "__all__"
