from __future__ import annotations

from clinicedc_constants import NOT_APPLICABLE
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.template.loader import render_to_string
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from meta_lists.constants import HEMACUE
from meta_lists.models import DiagnosticDevices

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
                    "fbg_diagnostic_device",
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
                    "ogtt_diagnostic_device",
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
        "fbg_diagnostic_device": admin.VERTICAL,
        "ogtt_diagnostic_device": admin.VERTICAL,
    }

    def get_list_display(self, request) -> tuple[str, ...]:
        list_display = super().get_list_display(request)
        list_display = list(list_display)
        list_display.insert(3, "ogtt_dx_device")
        list_display.insert(3, "fbg_dx_device")
        list_display.insert(3, "ogtt")
        list_display.insert(3, "fbg_value")
        list_display = [f for f in list_display if f != "__str__"]
        return tuple(list_display)

    def get_list_filter(self, request) -> tuple[str | type[SimpleListFilter], ...]:
        list_filter = super().get_list_filter(request)
        list_filter = list(list_filter)
        list_filter.insert(2, "fbg_diagnostic_device")
        list_filter.insert(2, "ogtt_diagnostic_device")
        list_filter.insert(2, OgttListFilter)
        list_filter.insert(2, FbgListFilter)
        return tuple(list_filter)

    @admin.display(description="FBG", ordering="fbg_value")
    def fbg(self, obj):
        return obj.fbg_value

    @admin.display(description="OGTT", ordering="ogtt_value")
    def ogtt(self, obj):
        return obj.ogtt_value

    def get_changeform_initial_data(self, request) -> dict:
        initial_data = super().get_changeform_initial_data(request)
        try:
            obj = DiagnosticDevices.objects.get(name=HEMACUE)
        except DiagnosticDevices.DoesNotExist:
            pass
        else:
            initial_data["fbg_diagnostic_device"] = obj.id
        try:
            obj = DiagnosticDevices.objects.get(name=NOT_APPLICABLE)
        except DiagnosticDevices.DoesNotExist:
            pass
        else:
            initial_data["ogtt_diagnostic_device"] = obj.id
        return initial_data

    @admin.display(description="FBG Device", ordering="fbg_diagnostic_device")
    def fbg_dx_device(self, obj=None):
        if obj:
            return obj.fbg_diagnostic_device
        return None

    @admin.display(description="OGTT Device", ordering="ogtt_diagnostic_device")
    def ogtt_dx_device(self, obj=None):
        if obj:
            return obj.fbg_diagnostic_device
        return None
