from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_lab_panel.panels import hba1c_panel, hba1c_poc_panel
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from ...models import BloodResultsHba1c


class BloodResultsHba1cFormValidator(BloodResultsFormValidatorMixin, CrfFormValidator):
    panels = [hba1c_poc_panel, hba1c_panel]


class BloodResultsHba1cForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsHba1cFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = BloodResultsHba1c
        fields = "__all__"
