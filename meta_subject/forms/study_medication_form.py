from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import StudyMedication


class StudyMedicationFormValidator(FormValidator):
    def clean(self):
        pass


class StudyMedicationForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = StudyMedicationFormValidator

    class Meta:
        model = StudyMedication
        fields = "__all__"
