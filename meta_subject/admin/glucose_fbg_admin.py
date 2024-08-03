from __future__ import annotations

from typing import Type

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django_audit_fields import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import GlucoseFbgForm
from ..models import GlucoseFbg
from .list_filters import GlucoseListFilter
from .modeladmin import CrfModelAdminMixin


@admin.register(GlucoseFbg, site=meta_subject_admin)
class GlucoseFbgAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    form = GlucoseFbgForm

    fieldsets = [
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
            "Confirmation appointment",
            {
                "description": (
                    "If blood glucose value is >= 7.0 mmol/L, schedule an "
                    "appointment within 1 week to confirm"
                ),
                "fields": ("repeat_fbg_date",),
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    ]

    radio_fields = {
        "fasting": admin.VERTICAL,
        "fbg_units": admin.VERTICAL,
        "fbg_performed": admin.VERTICAL,
    }

    @admin.display(description="FBG", ordering="fbg_value")
    def fbg(self, obj=None):
        return obj.fbg_value

    def get_list_display(self, request) -> tuple[str, ...]:
        list_display = super().get_list_display(request)
        list_display = list(list_display)
        # list_display.insert(3, "ogtt")
        list_display.insert(3, "fbg")
        list_display = tuple(list_display)
        return list_display

    def get_list_filter(self, request) -> tuple[str | Type[SimpleListFilter], ...]:
        list_filter = super().get_list_filter(request)
        list_filter = list(list_filter)
        list_filter.insert(2, GlucoseListFilter)
        list_filter = tuple(list_filter)
        return list_filter
