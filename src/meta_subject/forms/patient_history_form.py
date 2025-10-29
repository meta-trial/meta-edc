from clinicedc_constants import NO, NONE, OTHER, YES
from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import PatientHistory
from .mixins import ArvHistoryFormValidatorMixin


class PatientHistoryFormValidator(ArvHistoryFormValidatorMixin, CrfFormValidator):
    def clean(self):
        self.m2m_single_selection_if(NONE, m2m_field="symptoms")

        self.m2m_other_specify(OTHER, m2m_field="symptoms", field_other="other_symptoms")

        self.date_not_before(
            "hiv_diagnosis_date",
            "arv_initiation_date",
            "Invalid. Cannot be before HIV diagnosis date.",
        )

        self.validate_arv_history_fields()

        self.required_if(
            YES,
            field="on_htn_treatment",
            field_required="htn_treatment",
        )

        self.m2m_other_specify(
            OTHER,
            m2m_field="htn_treatment",
            field_other="other_htn_treatment",
        )

        self.applicable_if(
            YES,
            field="dyslipidaemia_diagnosis",
            field_applicable="on_dyslipidaemia_treatment",
        )

        self.applicable_if(
            YES,
            field="on_dyslipidaemia_treatment",
            field_applicable="dyslipidaemia_rx",
        )

        self.applicable_if(NO, field="current_smoker", field_applicable="former_smoker")

        self.m2m_single_selection_if(NONE, m2m_field="past_year_symptoms")
        self.m2m_other_specify(OTHER, m2m_field="dm_symptoms", field_other="other_dm_symptoms")


class PatientHistoryForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = PatientHistoryFormValidator

    class Meta:
        model = PatientHistory
        fields = "__all__"
