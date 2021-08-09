from django import forms
from edc_adherence.form_validator_mixin import MedicationAdherenceFormValidatorMixin
from edc_adherence.model_form_mixin import MedicationAdherenceFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import MedicationAdherence


class MedicationAdherenceFormValidator(
    MedicationAdherenceFormValidatorMixin, FormValidator
):
    pass


class MedicationAdherenceForm(
    MedicationAdherenceFormMixin, CrfModelFormMixin, forms.ModelForm
):

    form_validator_cls = MedicationAdherenceFormValidator

    class Meta:
        model = MedicationAdherence
        fields = "__all__"
