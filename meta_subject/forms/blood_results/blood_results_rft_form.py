from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from edc_lab_panel.panels import rft_panel
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin
from edc_reportable import BmiFormValidatorMixin

from ...models import BloodResultsRft


class BloodResultsRftFormValidator(
    BloodResultsFormValidatorMixin, BmiFormValidatorMixin, FormValidator
):
    panel = rft_panel

    def clean(self):
        super().clean()
        self.validate_bmi()


class BloodResultsRftForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsRftFormValidator

    class Meta:
        model = BloodResultsRft
        fields = "__all__"
