from django import forms
from edc_constants.constants import OTHER, NONE, NO, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import PatientHistory


class PatientHistoryFormValidator(FormValidator):
    def clean(self):

        self.m2m_single_selection_if(NONE, m2m_field="symptoms")

        self.m2m_other_specify(
            OTHER, m2m_field="symptoms", field_other="other_symptoms"
        )

        self.date_not_before(
            "hiv_diagnosis_date",
            "arv_initiation_date",
            "Invalid. Cannot be before HIV diagnosis date.",
        )

        self.date_not_before(
            "arv_initiation_date",
            "viral_load_date",
            "Invalid. Cannot be before ARV initiation date.",
        )

        self.date_not_before(
            "arv_initiation_date",
            "current_arv_regimen_date",
            "Invalid. Cannot be before ARV initiation date.",
        )

        self.required_if_not_none(
            "viral_load", "viral_load_date", field_required_evaluate_as_int=True
        )

        self.date_not_before(
            "hiv_diagnosis_date",
            "viral_load_date",
            "Invalid. Cannot be before HIV diagnosis date.",
        )

        self.required_if_not_none(
            "cd4", "cd4_date", field_required_evaluate_as_int=True
        )

        self.date_not_before(
            "hiv_diagnosis_date",
            "cd4_date",
            "Invalid. Cannot be before HIV diagnosis date.",
        )

        self.required_if(
            OTHER,
            field="current_arv_regimen",
            field_required="other_current_arv_regimen",
        )

        self.required_if(
            YES, field="has_previous_arv_regimen", field_required="previous_arv_regimen"
        )

        if self.cleaned_data.get("has_previous_arv_regimen") == NO:
            self.date_equal(
                "arv_initiation_date",
                "current_arv_regimen_start_date",
                "Invalid. Expected current regimen date to equal initiation date.",
            )

        self.required_if(
            YES, field="has_previous_arv_regimen", field_required="previous_arv_regimen"
        )

        self.required_if(
            OTHER,
            field="previous_arv_regimen",
            field_required="other_previous_arv_regimen",
        )

        self.required_if(
            YES, field="on_oi_prophylaxis", field_required="oi_prophylaxis"
        )

        self.m2m_other_specify(
            OTHER, m2m_field="oi_prophylaxis", field_other="other_oi_prophylaxis"
        )

        self.required_if(
            YES,
            field="on_hypertension_treatment",
            field_required="hypertension_treatment",
        )

        self.m2m_other_specify(
            OTHER,
            m2m_field="hypertension_treatment",
            field_other="other_hypertension_treatment",
        )

        self.applicable_if(NO, field="current_smoker", field_applicable="former_smoker")

        self.m2m_single_selection_if(NONE, m2m_field="past_year_symptoms")
        self.m2m_other_specify(
            OTHER, m2m_field="diabetes_symptoms", field_other="other_diabetes_symptoms"
        )


class PatientHistoryForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = PatientHistoryFormValidator

    class Meta:
        model = PatientHistory
        fields = "__all__"
