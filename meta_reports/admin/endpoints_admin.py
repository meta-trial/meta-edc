from django.contrib import admin
from django.db.models import QuerySet
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.admin import QaReportWithNoteModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from meta_analytics.dataframes import GlucoseEndpointsByDate

from ..admin_site import meta_reports_admin
from ..models import Endpoints


def generate_table(modeladmin, request, queryset):
    cls = GlucoseEndpointsByDate()
    df = cls.endpoint_only_df
    df["report_model"] = "meta_subject.endpoints"


generate_table.short_description = "Regenerate report data"


@admin.register(Endpoints, site=meta_reports_admin)
class EndpointAdmin(
    QaReportWithNoteModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    actions = [generate_table]
    qa_report_list_display_insert_pos = 2
    ordering = ["site", "subject_identifier"]
    list_display = [
        "dashboard",
        "subject",
        "visit_code",
        "fbg_datetime",
        "fasting",
        "fbg_value",
        "ogtt_value",
        "endpoint_label",
        "offstudy_datetime",
        "offstudy_reason",
        "created",
    ]

    list_filter = [
        "endpoint_label",
        ScheduleStatusListFilter,
    ]

    search_fields = ["subject_identifier"]

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        cls = GlucoseEndpointsByDate()
        df = cls.endpoint_only_df
        df["report_model"] = "meta_subject.endpoints"
        return qs
