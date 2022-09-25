from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_lab_panel.panels import lft_panel
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from ...models import BloodResultsLft


class BloodResultsLftFormValidator(BloodResultsFormValidatorMixin, CrfFormValidator):
    panel = lft_panel


class BloodResultsLftForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsLftFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = BloodResultsLft
        fields = "__all__"
