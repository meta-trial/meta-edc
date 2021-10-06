from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_blood_results.form_validator_mixins import BloodResultsFormValidatorMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from edc_lab_panel.panels import lft_panel

from meta_edc.meta_version import PHASE_TWO, get_meta_version
from meta_labs.lab_profiles import chemistry_panel

from ...models import BloodResultsLft


class BloodResultsLftFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panel = chemistry_panel if get_meta_version() == PHASE_TWO else lft_panel


class BloodResultsLftForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsLftFormValidator

    class Meta:
        model = BloodResultsLft
        fields = "__all__"
