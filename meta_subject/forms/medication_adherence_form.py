from django import forms
from edc_adherence.form_validator_mixin import MedicationAdherenceFormValidatorMixin
from edc_adherence.model_form_mixin import MedicationAdherenceFormMixin
from edc_constants.constants import YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_model.widgets import SliderWidget

from ..models import MedicationAdherence


class MedicationAdherenceFormValidator(
    MedicationAdherenceFormValidatorMixin, FormValidator
):
    def clean(self):
        self.required_if(YES, field="pill_count_performed", field_required="pill_count")


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
