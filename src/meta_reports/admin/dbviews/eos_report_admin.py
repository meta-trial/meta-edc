from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from ...admin_site import meta_reports_admin
from ...models import EosReport


@admin.register(EosReport, site=meta_reports_admin)
class EosReportAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    ordering = ("site", "subject_identifier", "offschedule_datetime")
    include_note_column = False
    list_display = (
        "dashboard",
        "subject_identifier_link",
        "site",
        "offschedule_datetime",
        "source",
    )

    list_filter = (
        "offschedule_datetime",
        "source",
    )

    search_fields = ("subject_identifier",)

    @admin.display(description="Subject Idenfifier", ordering="subject_identifier")
    def subject_identifier_link(self, obj=None):
        url = reverse("meta_reports_admin:meta_reports_eosreport_changelist")
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
        )
