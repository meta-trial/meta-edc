from django.conf import settings
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.urls import reverse
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.admin.list_filters import SiteListFilter
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ..tasks import update_endpoints_table


def update_endpoints_table_action(modeladmin, request, queryset):  # noqa: ARG001
    subject_identifiers = []
    if queryset.count() != modeladmin.model.objects.count():
        subject_identifiers = [o.subject_identifier for o in queryset]
    if settings.CELERY_ENABLED:
        return update_endpoints_table.delay(subject_identifiers)
    return update_endpoints_table(subject_identifiers)


update_endpoints_table_action.short_description = "Regenerate report for selected subjects"


class EndpointsModelAdminMixin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
):
    queryset_filter: dict | None = None
    actions = (update_endpoints_table_action,)
    qa_report_list_display_insert_pos = 3
    ordering = ("-fbg_date",)
    list_display = (
        "dashboard",
        "subject",
        "visit",
        "fbg_date",
        "fast",
        "fbg",
        "ogtt",
        "endpoint",
        "last_updated",
        "offstudy_date",
        "offstudy_reason",
    )

    list_filter = (
        "endpoint_label",
        ScheduleStatusListFilter,
        SiteListFilter,
    )

    search_fields = ("subject_identifier",)

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        if self.queryset_filter:
            qs = qs.filter(**self.queryset_filter)
        return qs

    def get_list_filter(self, request) -> tuple[str | type[SimpleListFilter], ...]:
        list_filter = super().get_list_filter(request)
        return *list_filter, SiteListFilter

    @admin.display(description="subject", ordering="subject_identifier")
    def subject(self, obj=None):
        return obj.subject_identifier

    @admin.display(description="visit", ordering="visit_code")
    def visit(self, obj=None):
        return obj.visit_code

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
        url = reverse("meta_reports_admin:meta_reports_glucosesummary_changelist")
        return render_to_string(
            "meta_reports/columns/subject_identifier_column.html",
            {
                "subject_identifier": obj.subject_identifier,
                "url": url,
                "label": obj.endpoint_label,
            },
        )

    @admin.display(description="last_updated", ordering="created")
    def last_updated(self, obj=None):
        return obj.created
