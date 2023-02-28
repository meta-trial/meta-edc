from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_lab_panel.panels import lipids_panel
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from ...models import BloodResultsLipid


class BloodResultsLipidFormValidator(BloodResultsFormValidatorMixin, CrfFormValidator):
    panel = lipids_panel


class BloodResultsLipidForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = BloodResultsLipidFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = BloodResultsLipid
        fields = "__all__"
