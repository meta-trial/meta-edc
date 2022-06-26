from copy import copy

from django.contrib import admin
from django.utils.html import format_html
from edc_action_item import action_fields, action_fieldset_tuple
from edc_constants.constants import CLOSED, OPEN
from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin, audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import meta_prn_admin
from ..forms import ProtocolIncidentForm
from ..models import ProtocolIncident


@admin.register(ProtocolIncident, site=meta_prn_admin)
class ProtocolDeviationViolationAdmin(
    DataManagerModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = ProtocolIncidentForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "report_datetime",
                    "short_description",
                    "report_type",
                )
            },
        ),
        (
            "Details of incident",
            {
                "fields": (
                    "safety_impact",
                    "safety_impact_details",
                    "study_outcomes_impact",
                    "study_outcomes_impact_details",
                    "incident_datetime",
                    "incident",
                    "incident_other",
                    "incident_description",
                    "incident_reason",
                ),
            },
        ),
        (
            "Actions taken",
            {
                "description": (
                    "The following questions are required before the report is closed."
                ),
                "fields": (
                    "corrective_action_datetime",
                    "corrective_action",
                    "preventative_action_datetime",
                    "preventative_action",
                    "action_required",
                ),
            },
        ),
        ("Report status", {"fields": ("report_status", "report_closed_datetime")}),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "action_required": admin.VERTICAL,
        "report_status": admin.VERTICAL,
        "report_type": admin.VERTICAL,
        "safety_impact": admin.VERTICAL,
        "study_outcomes_impact": admin.VERTICAL,
        "incident": admin.VERTICAL,
    }

    list_display = (
        "subject_identifier",
        "dashboard",
        "description",
        "report_datetime",
        "status",
        "action_required",
        "report_type",
        "tracking_identifier",
        "action_identifier",
        "user_created",
    )

    list_filter = ("action_required", "report_status", "report_type")

    search_fields = [
        "subject_identifier",
        "action_identifier",
        "short_description",
        "tracking_identifier",
    ]

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        action_flds.remove("action_identifier")
        fields = list(action_flds) + list(fields)
        return fields

    def status(self, obj=None):
        if obj.report_status == CLOSED:
            return format_html(f'<font color="green">{obj.report_status.title()}</font>')
        elif obj.report_status == OPEN:
            return format_html(f'<font color="red">{obj.report_status.title()}</font>')
        return obj.report_status.title()

    def description(self, obj=None):
        return obj.short_description.title()
