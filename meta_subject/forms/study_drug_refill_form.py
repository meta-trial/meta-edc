from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import StudyDrugRefill


class StudyDrugRefillFormValidator(FormValidator):
    def clean(self):
        pass


class StudyDrugRefillForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = StudyDrugRefillFormValidator

    class Meta:
        model = StudyDrugRefill
        fields = "__all__"
