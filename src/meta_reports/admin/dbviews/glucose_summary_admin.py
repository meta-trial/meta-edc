from clinicedc_constants import YES
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from edc_glucose.list_filters import FbgListFilter, OgttListFilter
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ...admin_site import meta_reports_admin
from ...models import Endpoints, EndpointsProxy, GlucoseSummary
from ..list_filters import EndpointListFilter


@admin.register(GlucoseSummary, site=meta_reports_admin)
class GlucoseSummaryAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    ordering = ("site", "subject_identifier", "fbg_datetime")
    include_note_column = False
    list_display = (
        "dashboard",
        "subject_identifier_link",
        "site",
        "visit",
        "fasted",
        "fbg_date",
        "fbg_value",
        "ogtt_value",
        "ogtt_date",
        "endpoint",
        "offstudy_date",
    )

    list_filter = (
        ScheduleStatusListFilter,
        "fasted",
        FbgListFilter,
        OgttListFilter,
        "fbg_datetime",
        "ogtt_datetime",
        EndpointListFilter,
    )

    search_fields = ("subject_identifier",)

    @admin.display(description="visit", ordering="visit_code")
    def visit(self, obj=None):
        return f"{obj.visit_code}.{obj.visit_code_sequence}"

    @admin.display(description="Endpoint")
    def endpoint(self, obj=None):
        try:
            endpoint_obj = Endpoints.objects.get(subject_identifier=obj.subject_identifier)
        except ObjectDoesNotExist:
            value = None
        else:
            if endpoint_obj.offstudy_date:
                url = reverse("meta_reports_admin:meta_reports_endpointsproxy_changelist")
                title = f"Go to {EndpointsProxy._meta.verbose_name}"
            else:
                url = reverse("meta_reports_admin:meta_reports_endpoints_changelist")
                title = f"Go to {Endpoints._meta.verbose_name}"
            value = render_to_string(
                "meta_reports/columns/subject_identifier_column.html",
                {
                    "subject_identifier": obj.subject_identifier,
                    "url": url,
                    "label": YES,
                    "title": title,
                },
            )
        return value

    @admin.display(description="Subject Idenfifier", ordering="subject_identifier")
    def subject_identifier_link(self, obj=None):
        url = reverse("meta_reports_admin:meta_reports_glucosesummary_changelist")
        return render_to_string(
            "meta_reports/columns/subject_identifier_column.html",
            {
                "subject_identifier": obj.subject_identifier,
                "url": url,
                "title": "Click to filter for this subject only",
            },
        )

    def get_subject_dashboard_url_kwargs(self, obj) -> dict:
        return dict(
            subject_identifier=obj.subject_identifier,
            appointment=obj.appointment_id,
        )

    @admin.display(description="Fbg date", ordering="fbg_datetime")
    def fbg_date(self, obj):
        if obj.fbg_datetime:
            return obj.fbg_datetime.date()
        return None

    @admin.display(description="OGTT date", ordering="ogtt_datetime")
    def ogtt_date(self, obj):
        if obj.ogtt_datetime:
            return obj.ogtt_datetime.date()
        return None

    @admin.display(description="Offstudy date", ordering="offstudy_datetime")
    def offstudy_date(self, obj):
        if obj.offstudy_datetime:
            return obj.offstudy_datetime.date()
        return None
