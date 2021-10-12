from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_blood_results.form_validator_mixins import (
    BloodResultsFormValidatorMixin,
    BloodResultsGluFormValidatorMixin,
)
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from edc_lab_panel.panels import blood_glucose_panel, blood_glucose_poc_panel

from meta_edc.meta_version import PHASE_TWO, get_meta_version

from ...models import BloodResultsGlu


class BloodResultsGluFormValidator(
    BloodResultsGluFormValidatorMixin, BloodResultsFormValidatorMixin, FormValidator
):
    panel = (
        blood_glucose_poc_panel
        if get_meta_version() == PHASE_TWO
        else blood_glucose_panel
    )


class BloodResultsGluForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsGluFormValidator

    class Meta:
        model = BloodResultsGlu
        fields = "__all__"
