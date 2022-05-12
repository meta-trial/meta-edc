from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from edc_lab_panel.panels import insulin_panel
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from ...models import BloodResultsIns


class BloodResultsInsFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panel = insulin_panel


class BloodResultsInsForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsInsFormValidator

    class Meta:
        model = BloodResultsIns
        fields = "__all__"
