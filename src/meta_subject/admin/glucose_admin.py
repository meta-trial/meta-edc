from __future__ import annotations

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.template.loader import render_to_string
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import GlucoseForm
from ..models import Glucose
from .list_filters import FbgListFilter, OgttListFilter
from .modeladmin import CrfModelAdminMixin


@admin.register(Glucose, site=meta_subject_admin)
class GlucoseAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    form = GlucoseForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Fasting",
            {
                "fields": (
                    "fasting",
                    "fasting_duration_str",
                )
            },
        ),
        (
            "Blood Glucose",
            {
                "fields": (
                    "fbg_performed",
                    "fbg_not_performed_reason",
                    "fbg_datetime",
                    "fbg_value",
                    "fbg_units",
                )
            },
        ),
        (
            "OGTT",
            {
                "fields": (
                    "ogtt_performed",
                    "ogtt_not_performed_reason",
                    "ogtt_base_datetime",
                    "ogtt_datetime",
                    "ogtt_value",
                    "ogtt_units",
                )
            },
        ),
        (
            "Endpoint review",
            {
                "description": render_to_string(
                    "meta_subject/endpoint_review_instructions.html", context={}
                ),
                "fields": (
                    "endpoint_today",
                    "repeat_fbg_date",
                ),
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "fasting": admin.VERTICAL,
        "fbg_units": admin.VERTICAL,
        "fbg_performed": admin.VERTICAL,
        "ogtt_performed": admin.VERTICAL,
        "ogtt_units": admin.VERTICAL,
        "endpoint_today": admin.VERTICAL,
    }

    def get_list_display(self, request) -> tuple[str, ...]:
        list_display = super().get_list_display(request)
        list_display = list(list_display)
        list_display.insert(3, "ogtt_value")
        list_display.insert(3, "fbg_value")
        return tuple(list_display)

    def get_list_filter(self, request) -> tuple[str | type[SimpleListFilter], ...]:
        list_filter = super().get_list_filter(request)
        list_filter = list(list_filter)
        list_filter.insert(2, OgttListFilter)
        list_filter.insert(2, FbgListFilter)
        return tuple(list_filter)
