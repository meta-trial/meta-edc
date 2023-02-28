from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_lab_panel.panels import insulin_panel
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from ...models import BloodResultsIns


class BloodResultsInsFormValidator(BloodResultsFormValidatorMixin, CrfFormValidator):
    panel = insulin_panel


class BloodResultsInsForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = BloodResultsInsFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = BloodResultsIns
        fields = "__all__"
