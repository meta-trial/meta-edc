from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import ConcomitantMedication


class ConcomitantMedicationFormValidator(FormValidator):
    def clean(self):
        pass


class ConcomitantMedicationForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = ConcomitantMedicationFormValidator

    class Meta:
        model = ConcomitantMedication
        fields = "__all__"
