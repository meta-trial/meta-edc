from django import forms
from edc_adherence.form_validator_mixin import MedicationAdherenceFormValidatorMixin
from edc_adherence.model_form_mixin import MedicationAdherenceFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_model.widgets import SliderWidget

from ..models import MedicationAdherence


class MedicationAdherenceFormValidator(
    MedicationAdherenceFormValidatorMixin, CrfFormValidator
):
    pass


class MedicationAdherenceForm(
    MedicationAdherenceFormMixin, CrfModelFormMixin, forms.ModelForm
):

    form_validator_cls = MedicationAdherenceFormValidator

    visual_score_slider = forms.CharField(
        label="Visual Score", widget=SliderWidget(attrs={"min": 0, "max": 100})
    )

    class Meta:
        model = MedicationAdherence
        fields = "__all__"
