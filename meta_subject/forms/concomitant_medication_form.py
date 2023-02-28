from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import ConcomitantMedication


class ConcomitantMedicationFormValidator(CrfFormValidator):
    def clean(self):
        pass


class ConcomitantMedicationForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ConcomitantMedicationFormValidator

    class Meta:
        model = ConcomitantMedication
        fields = "__all__"
