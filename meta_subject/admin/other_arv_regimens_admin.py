from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import ArvHistoryForm
from ..models import ArvHistory
from .modeladmin import CrfModelAdmin


@admin.register(ArvHistory, site=meta_subject_admin)
class ArvHistoryAdmin(CrfModelAdmin):

    form = ArvHistoryForm

    autocomplete_fields = ["current_arv_regimen", "previous_arv_regimen"]
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "HIV, ARVs and other prophylaxis",
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
        audit_fieldset_tuple,
    )

    radio_fields = {
        "current_arv_regimen": admin.VERTICAL,
        "has_previous_arv_regimen": admin.VERTICAL,
        "on_oi_prophylaxis": admin.VERTICAL,
        "previous_arv_regimen": admin.VERTICAL,
    }

    filter_horizontal = (
        "oi_prophylaxis",
        "hiv_diagnosis_date",
        "arv_initiation_date",
    )
