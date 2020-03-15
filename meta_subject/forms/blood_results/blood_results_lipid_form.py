from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_action_item.forms import ActionItemFormMixin
from meta_form_validators.form_validators import BloodResultsLipidFormValidator

from ...models import BloodResultsLipid


class BloodResultsLipidForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsLipidFormValidator

    class Meta:
        model = BloodResultsLipid
        fields = "__all__"
