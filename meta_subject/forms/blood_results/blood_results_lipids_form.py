from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_lab_panel.panels import lipids_panel
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from ...models import BloodResultsLipids


class BloodResultsLipidsFormValidator(BloodResultsFormValidatorMixin, CrfFormValidator):
    panel = lipids_panel


class BloodResultsLipidsForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = BloodResultsLipidsFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = BloodResultsLipids
        fields = "__all__"
