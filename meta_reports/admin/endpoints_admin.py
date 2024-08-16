from typing import Type

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.admin.list_filters import SiteListFilter
from edc_visit_schedule.admin import ScheduleStatusListFilter

from meta_analytics.dataframes import GlucoseEndpointsByDate

from ..admin_site import meta_reports_admin
from ..models import Endpoints


def generate_table(modeladmin, request, queryset):
    cls = GlucoseEndpointsByDate()
    cls.run()
    cls.to_model()


generate_table.short_description = "Regenerate report data"


@admin.register(Endpoints, site=meta_reports_admin)
class EndpointAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    actions = [generate_table]
    qa_report_list_display_insert_pos = 2
    ordering = ["-fbg_datetime"]
    list_display = [
        "dashboard",
        "subject",
        "visit",
        "fbg_date",
        "fast",
        "fbg",
        "ogtt",
        "endpoint",
        "last_updated",
        "offstudy_datetime",
        "offstudy_reason",
    ]

    list_filter = [
        "endpoint_label",
        ScheduleStatusListFilter,
        SiteListFilter,
    ]

    search_fields = ["subject_identifier"]

    def get_list_filter(self, request) -> tuple[str | Type[SimpleListFilter], ...]:
        list_filter = super().get_list_filter(request)
        list_filter = list_filter + (SiteListFilter,)
        return list_filter

    @admin.display(description="subject", ordering="subject_identifier")
    def subject(self, obj=None):
        return obj.subject_identifier

    @admin.display(description="visit", ordering="visit_code")
    def visit(self, obj=None):
        return obj.visit_code

    @admin.display(description="FBG DATE", ordering="fbg_datetime")
    def fbg_date(self, obj=None):
        return obj.fbg_datetime.date() if obj.fbg_datetime else None

    @admin.display(description="FAST", ordering="fasting")
    def fast(self, obj=None):
        return obj.fasting

    @admin.display(description="FBG", ordering="fbg_value")
    def fbg(self, obj=None):
        return obj.fbg_value

    @admin.display(description="OGTT", ordering="ogtt_value")
    def ogtt(self, obj=None):
        return obj.ogtt_value

    @admin.display(description="endpoint", ordering="endpoint_label")
    def endpoint(self, obj=None):
        return obj.endpoint_label

    @admin.display(description="last_updated", ordering="created")
    def last_updated(self, obj=None):
        return obj.created
