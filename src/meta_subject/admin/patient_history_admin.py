from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import PatientHistoryForm
from ..models import PatientHistory
from .fieldsets import get_hiv_fieldset, get_htn_fieldset, get_other_history_fieldset
from .modeladmin import CrfModelAdminMixin


@admin.register(PatientHistory, site=meta_subject_admin)
class PatientHistoryAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    form = PatientHistoryForm

    autocomplete_fields = ("current_arv_regimen", "previous_arv_regimen")
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Part 1: Symptoms", {"fields": ("symptoms", "other_symptoms")}),
        get_hiv_fieldset(part="2"),
        get_htn_fieldset(part="3"),
        get_other_history_fieldset(part="4"),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "current_arv_regimen": admin.VERTICAL,
        "current_smoker": admin.VERTICAL,
        "dm_in_family": admin.VERTICAL,
        "dyslipidaemia_diagnosis": admin.VERTICAL,
        "dyslipidaemia_rx": admin.VERTICAL,
        "former_smoker": admin.VERTICAL,
        "has_previous_arv_regimen": admin.VERTICAL,
        "htn_diagnosis": admin.VERTICAL,
        "on_dyslipidaemia_treatment": admin.VERTICAL,
        "on_htn_treatment": admin.VERTICAL,
        "on_oi_prophylaxis": admin.VERTICAL,
        "previous_arv_regimen": admin.VERTICAL,
        "taking_statins": admin.VERTICAL,
    }

    filter_horizontal = (
        "symptoms",
        "oi_prophylaxis",
        "dm_symptoms",
        "htn_treatment",
    )
