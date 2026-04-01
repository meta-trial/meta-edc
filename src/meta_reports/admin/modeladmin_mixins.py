from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.contrib.messages.constants import INFO
from django.db.models import Min, QuerySet
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from edc_data_manager.auth_objects import DATA_MANAGER_ROLE
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.admin.list_filters import SitesForDataManagerListFilter
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
        "subject_review_dashboard",
        "subject",
        "visit",
        "fbg_date",
        "fast",
        "hrs",
        "fbg",
        "ogtt",
        "endpoint",
        "referral",
        "last_updated",
        "offstudy_date",
        "offstudy_reason",
    )

    list_filter = (
        "endpoint_label",
        ScheduleStatusListFilter,
    )

    search_fields = ("subject_identifier",)

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        if (
            qs.count() == 0
            or (timezone.now() - qs.aggregate(Min("created")).get("created__min")).days > 0
        ):
            update_endpoints_table()
            messages.add_message(request, INFO, "Endpoint data has just been updated.")
        if self.queryset_filter:
            qs = qs.filter(**self.queryset_filter)
        return qs

    def get_list_filter(self, request) -> tuple[str | type[SimpleListFilter], ...]:
        list_filter = super().get_list_filter(request)
        return *list_filter, SitesForDataManagerListFilter

    @admin.display(description="subject", ordering="subject_identifier")
    def subject(self, obj=None):
        return obj.subject_identifier

    @admin.display(description="visit", ordering="visit_code")
    def visit(self, obj=None):
        return obj.visit_code

    @admin.display(description="FAST", ordering="fasting")
    def fast(self, obj=None):
        return obj.fasting

    @admin.display(description="HRS", ordering="fasted_hrs")
    def hrs(self, obj=None):
        return obj.fasted_hrs

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

    @admin.display(description="Referral", ordering="referral_date")
    def referral(self, obj=None):
        if obj and obj.referral_date:
            url = reverse("meta_prn_admin:meta_prn_dmreferral_changelist")
            return format_html(
                '<A href="{url}?q={subject_identifier}">{referral_date}</A>',
                url=url,
                referral_date=obj.referral_date,
                subject_identifier=obj.subject_identifier,
            )
        return None

    def get_view_only_site_ids_for_user(self, request) -> list[int]:
        if request.user.userprofile.roles.filter(name=DATA_MANAGER_ROLE).exists():
            return [
                s.id for s in request.user.userprofile.sites.all() if s.id != request.site.id
            ]
        return super().get_view_only_site_ids_for_user(request)
