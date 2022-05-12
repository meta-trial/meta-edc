from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from edc_lab_panel.panels import blood_glucose_panel
from edc_lab_results.form_validator_mixins import (
    BloodResultsFormValidatorMixin,
    BloodResultsGluFormValidatorMixin,
)

from ...models import BloodResultsGlu


class BloodResultsGluFormValidator(
    BloodResultsGluFormValidatorMixin, BloodResultsFormValidatorMixin, FormValidator
):
    panel = blood_glucose_panel


class BloodResultsGluForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsGluFormValidator

    class Meta:
        model = BloodResultsGlu
        fields = "__all__"
