from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import ArvHistory
from .mixins import ArvHistoryFormValidatorMixin


class ArvHistoryFormValidator(ArvHistoryFormValidatorMixin, FormValidator):
    def clean(self):

        self.validate_arv_history_fields()


class ArvHistoryForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = ArvHistoryFormValidator

    class Meta:
        model = ArvHistory
        fields = "__all__"
