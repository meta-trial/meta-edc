from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_glucose.form_validators import FbgOgttFormValidatorMixin

from ..models import Glucose


class GlucoseFormValidator(FbgOgttFormValidatorMixin, CrfFormValidator):
    def clean(self):
        self.validate_glucose_testing_matrix()


class GlucoseForm(CrfModelFormMixin, ActionItemCrfFormMixin, forms.ModelForm):
    form_validator_cls = GlucoseFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = Glucose
        fields = "__all__"
