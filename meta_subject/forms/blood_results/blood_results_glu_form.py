from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_lab_panel.panels import blood_glucose_panel
from edc_lab_results.form_validator_mixins import (
    BloodResultsFormValidatorMixin,
    BloodResultsGluFormValidatorMixin,
)

from ...models import BloodResultsGlu


class BloodResultsGluFormValidator(
    BloodResultsGluFormValidatorMixin, BloodResultsFormValidatorMixin, CrfFormValidator
):
    panel = blood_glucose_panel


class BloodResultsGluForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsGluFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = BloodResultsGlu
        fields = "__all__"
