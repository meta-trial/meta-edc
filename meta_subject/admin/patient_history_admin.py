from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import PatientHistoryForm
from ..models import PatientHistory
from .modeladmin import CrfModelAdmin


@admin.register(PatientHistory, site=meta_subject_admin)
class PatientHistoryAdmin(CrfModelAdmin):

    form = PatientHistoryForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Part 1: Symptoms", {"fields": ("symptoms", "other_symptoms")}),
        (
            "Part 2: HIV, ARVs and other prophylaxis",
            {
                "fields": (
                    "hiv_diagnosis_date",
                    "arv_initiation_date",
                    "viral_load",
                    "viral_load_date",
                    "cd4",
                    "cd4_date",
                    "current_arv_regimen",
                    "other_current_arv_regimen",
                    "current_arv_regimen_start_date",
                    "has_previous_arv_regimen",
                    "previous_arv_regimen",
                    "other_previous_arv_regimen",
                    "on_oi_prophylaxis",
                    "oi_prophylaxis",
                    "other_oi_prophylaxis",
                )
            },
        ),
        (
            "Part 3: Hypertension",
            {
                "fields": (
                    "hypertension_diagnosis",
                    "on_hypertension_treatment",
                    "hypertension_treatment",
                    "other_hypertension_treatment",
                    "taking_statins",
                )
            },
        ),
        (
            "Part 4: Other history",
            {
                "fields": (
                    "current_smoker",
                    "former_smoker",
                    "diabetes_symptoms",
                    "other_diabetes_symptoms",
                    "diabetes_in_family",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "current_arv_regimen": admin.VERTICAL,
        "current_smoker": admin.VERTICAL,
        "diabetes_in_family": admin.VERTICAL,
        "former_smoker": admin.VERTICAL,
        "has_previous_arv_regimen": admin.VERTICAL,
        "hypertension_diagnosis": admin.VERTICAL,
        "on_hypertension_treatment": admin.VERTICAL,
        "on_oi_prophylaxis": admin.VERTICAL,
        "previous_arv_regimen": admin.VERTICAL,
        "taking_statins": admin.VERTICAL,
    }

    filter_horizontal = (
        "symptoms",
        "oi_prophylaxis",
        "diabetes_symptoms",
        "hypertension_treatment",
    )
