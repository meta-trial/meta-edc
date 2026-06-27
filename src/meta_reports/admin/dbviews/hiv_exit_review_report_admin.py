import re

from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from edc_appointment.models import Appointment
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_protocol.research_protocol_config import ResearchProtocolConfig
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from rangefilter.filters import DateRangeFilterBuilder

from ...admin_site import meta_reports_admin
from ...forms import HivExitReviewReportForm
from ...models import HivExitReviewReport
from ..list_filters import IsOffScheduleListFilter


@admin.register(HivExitReviewReport, site=meta_reports_admin)
class HivExitReviewReportAdmin(
    # ExportMixin,
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    ordering = ("site", "subject_identifier", "offschedule_datetime")
    include_note_column = False
    list_per_page = 10

    form = HivExitReviewReportForm

    change_list_note = (
        "View subjects without an HIV Exit Review form. "
        "Visit is the next or last visit. Hospital identifier is not searchable."
    )

    list_filter = (
        "appt_status",
        ("offschedule_datetime", DateRangeFilterBuilder()),
        ("appt_datetime", DateRangeFilterBuilder()),
        IsOffScheduleListFilter,
        "visit_code",
        "source",
    )

    search_fields = ("subject_identifier",)

    list_display_links = ("subject_identifier",)

    @admin.display(description="Subject ID", ordering="subject_identifier")
    def subject_identifier_link(self, obj=None):
        url = reverse("meta_reports_admin:meta_reports_hivexitreviewreport_changelist")
        return render_to_string(
            "meta_reports/columns/subject_identifier_column.html",
            {
                "subject_identifier": obj.subject_identifier,
                "url": url,
                "title": "Click to filter for this subject only",
            },
        )

    def get_subject_dashboard_url_kwargs(self, obj) -> dict:
        if appt := (
            Appointment.objects.filter(
                subject_identifier=obj.subject_identifier,
                visit_schedule_name=obj.visit_schedule_name,
                schedule_name=obj.schedule_name,
                subjectvisit__isnull=False,
            )
            .order_by("appt_datetime")
            .last()
        ):
            return dict(
                subject_identifier=obj.subject_identifier,
                appointment=appt.id,
            )
        return dict(
            subject_identifier=obj.subject_identifier,
        )

    def get_list_display(self, request):
        MASK = "*****"  # noqa: N806
        pattern = ResearchProtocolConfig().subject_identifier_pattern
        query = request.GET.get("q", "").strip()
        seacrh_active = re.match(pattern, query)

        @admin.display(description="Initials")
        def masked_initials(obj) -> str:
            return obj.initials if seacrh_active else MASK

        @admin.display(description="Lastname")
        def masked_last_name(obj) -> str:
            return obj.last_name if seacrh_active else MASK

        @admin.display(description="Hospital ID")
        def masked_hospital_identifier(obj) -> str:
            return obj.hospital_identifier if seacrh_active else MASK

        return (
            "dashboard",
            "subject_identifier_link",
            masked_initials,
            masked_last_name,
            masked_hospital_identifier,
            "site",
            "offschedule_date",
            "visit_code",
            "appt_date",
            "days",
            "appt_status",
            "source",
        )

    @admin.display(description="Name")
    def name(self, obj=None) -> str | None:
        return f"{obj.last_name}, {obj.first_name}"
        # return None

    @admin.display(description="Appt date", ordering="appt_datetime")
    def appt_date(self, obj):
        if obj and obj.appt_datetime:
            return obj.appt_datetime.date()
        return None

    @admin.display(description="Offschedule date", ordering="offschedule_datetime")
    def offschedule_date(self, obj):
        if obj and obj.offschedule_datetime:
            return obj.offschedule_datetime.date()
        return None
