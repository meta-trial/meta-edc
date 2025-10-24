from __future__ import annotations

from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import HivExitReviewForm
from ..models import HivExitReview
from .modeladmin import CrfModelAdminMixin


@admin.register(HivExitReview, site=meta_subject_admin)
class HivExitReviewAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    autocomplete_fields = ("current_arv_regimen",)

    form = HivExitReviewForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "available",
                    "not_available_reason",
                )
            },
        ),
        (
            "HIV and ARVs",
            {
                "fields": (
                    "viral_load",
                    "viral_load_date",
                    "cd4",
                    "cd4_date",
                    "current_arv_regimen",
                    "other_current_arv_regimen",
                    "current_arv_regimen_start_date",
                )
            },
        ),
        ("Comment", {"fields": ("comment",)}),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    list_filter = ("available",)

    radio_fields = {  # noqa: RUF012
        "available": admin.VERTICAL,
    }
