import contextlib
from decimal import Decimal

from clinicedc_constants import YES
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from edc_data_manager.auth_objects import DATA_MANAGER_ROLE
from edc_glucose.list_filters import FbgListFilter, OgttListFilter
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.admin.list_filters import SitesForDataManagerListFilter
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ...admin_site import meta_reports_admin
from ...models import Endpoints, EndpointsProxy, GlucoseSummary
from ..list_filters import EndpointListFilter, OnlyEndpointListFilter


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
        "subject_review_dashboard",
        "subject_identifier_link",
        "endpoint",
        "site",
        "visit",
        "fasted",
        "hrs",
        "fbg_date",
        "fbg",
        "ogtt",
        "ogtt_date",
        "offstudy_date",
    )

    list_filter = (
        ScheduleStatusListFilter,
        "fasted",
        FbgListFilter,
        OgttListFilter,
        "fbg_datetime",
        "ogtt_datetime",
        OnlyEndpointListFilter,
        EndpointListFilter,
        SitesForDataManagerListFilter,
    )

    search_fields = ("subject_identifier",)

    @admin.display(description="Fbg", ordering="fbg_value")
    def fbg(self, obj=None):
        if obj and obj.fasted == YES:
            return obj.fbg_value
        return None

    @admin.display(description="OGTT", ordering="ogtt_value")
    def ogtt(self, obj=None):
        if obj and obj.fasted == YES:
            return obj.ogtt_value
        return None

    @admin.display(description="HRS", ordering="fasting_duration_delta")
    def hrs(self, obj=None):
        if obj.fasting_duration_delta:
            return round(obj.fasting_duration_delta.seconds / 3600, 1)
        return None

    @admin.display(description="visit", ordering="visit_code")
    def visit(self, obj=None):
        if self.get_endpoint(obj=obj):
            return format_html(
                '<span style="background-color: #FFDDDD;">{}.{}</span>',
                obj.visit_code,
                obj.visit_code_sequence,
            )
        return f"{obj.visit_code}.{obj.visit_code_sequence}"

    @staticmethod
    def get_endpoint(obj=None):
        endpoint_obj = None
        if obj:
            with contextlib.suppress(ObjectDoesNotExist):
                endpoint_obj = Endpoints.objects.get(
                    subject_identifier=obj.subject_identifier,
                    visit_code=Decimal(f"{obj.visit_code}.{obj.visit_code_sequence}"),
                )
        return endpoint_obj

    @admin.display(description="Endpoint")
    def endpoint(self, obj=None):
        value = None
        if self.get_endpoint(obj=obj):
            url = reverse("meta_reports_admin:meta_reports_endpointsproxy_changelist")
            title = f"Go to {EndpointsProxy._meta.verbose_name}"
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

    def get_view_only_site_ids_for_user(self, request) -> list[int]:
        if request.user.userprofile.roles.filter(name=DATA_MANAGER_ROLE).exists():
            return [
                s.id for s in request.user.userprofile.sites.all() if s.id != request.site.id
            ]
        return super().get_view_only_site_ids_for_user(request)
