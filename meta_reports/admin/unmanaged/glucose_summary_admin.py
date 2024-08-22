from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from edc_constants.constants import YES
from edc_glucose.list_filters import FbgListFilter, OgttListFilter
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ...admin_site import meta_reports_admin
from ...models import Endpoints, GlucoseSummary
from ..list_filters import EndpointListFilter


@admin.register(GlucoseSummary, site=meta_reports_admin)
class GlucoseSummaryAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    ordering = ["site", "subject_identifier", "fbg_datetime"]
    include_note_column = False
    list_display = [
        "dashboard",
        "subject_identifier_link",
        "site",
        "visit",
        "fbg_datetime",
        "fbg_value",
        "ogtt_value",
        "ogtt_datetime",
        "endpoint",
    ]

    list_filter = [
        ScheduleStatusListFilter,
        FbgListFilter,
        OgttListFilter,
        "fbg_datetime",
        "ogtt_datetime",
        EndpointListFilter,
    ]

    search_fields = ["subject_identifier"]

    @admin.display(description="visit", ordering="visit_code")
    def visit(self, obj=None):
        return f"{obj.visit_code}.{obj.visit_code_sequence}"

    @admin.display(description="Endpoint")
    def endpoint(self, obj=None):
        if Endpoints.objects.filter(subject_identifier=obj.subject_identifier).exists():
            url = reverse("meta_reports_admin:meta_reports_endpoints_changelist")
            return render_to_string(
                "meta_reports/columns/subject_identifier_column.html",
                {"subject_identifier": obj.subject_identifier, "url": url, "label": YES},
            )
        return None

    @admin.display(description="Subject Idenfifier", ordering="subject_identifier")
    def subject_identifier_link(self, obj=None):
        url = reverse("meta_reports_admin:meta_reports_glucosesummary_changelist")
        return render_to_string(
            "meta_reports/columns/subject_identifier_column.html",
            {"subject_identifier": obj.subject_identifier, "url": url},
        )

    def get_subject_dashboard_url_kwargs(self, obj) -> dict:
        return dict(
            subject_identifier=obj.subject_identifier,
            appointment=obj.appointment_id,
        )
