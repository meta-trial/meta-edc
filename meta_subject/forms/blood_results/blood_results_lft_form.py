from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_blood_results.form_validator_mixins import BloodResultsFormValidatorMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from edc_lab_panel.panels import lft_panel

from ...models import BloodResultsLft


class BloodResultsLftFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panel = lft_panel


class BloodResultsLftForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsLftFormValidator

    class Meta:
        model = BloodResultsLft
        fields = "__all__"
