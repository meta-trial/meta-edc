from django.contrib import admin
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from rangefilter.filters import DateRangeFilterBuilder

from ...admin_site import meta_reports_admin
from ...forms import HivExitReviewReportForm
from ...models import HivExitReviewReport
from ..list_filters import IsOffScheduleListFilter


@admin.register(HivExitReviewReport, site=meta_reports_admin)
class HivExitReviewReportAdmin(
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

    list_display = (
        "dashboard",
        "subject_identifier",
        "hospital_identifier",
        "site",
        "offschedule_date",
        "visit_code",
        "appt_date",
        "days",
        "appt_status",
        "source",
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

    # @admin.display(description="Subject Identifier", ordering="subject_identifier")
    # def subject_identifier_link(self, obj=None):
    #     url = reverse("meta_reports_admin:meta_reports_hivexitreviewreport_changelist")
    #     return render_to_string(
    #         "meta_reports/columns/subject_identifier_column.html",
    #         {
    #             "subject_identifier": obj.subject_identifier,
    #             "url": url,
    #             "title": "Click to filter for this subject only",
    #         },
    #     )

    def get_subject_dashboard_url_kwargs(self, obj) -> dict:
        return dict(
            subject_identifier=obj.subject_identifier,
        )

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
