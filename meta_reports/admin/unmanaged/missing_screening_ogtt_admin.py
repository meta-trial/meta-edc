from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ...admin_site import meta_reports_admin
from ...models import MissingScreeningOgtt


@admin.register(MissingScreeningOgtt, site=meta_reports_admin)
class MissingScreeningOgttAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    ordering = ["site", "screening_identifier"]
    list_display = [
        "dashboard",
        "screening_identifier",
        "site",
        "screening_datetime",
        "fbg_datetime",
        "fbg_value",
        "ogtt_value",
        "repeated",
        "p3_ltfu",
        "fbg2_value",
        "ogtt2_value",
        "fbg2_datetime",
        "ogtt2_datetime",
        "consented",
    ]

    list_filter = [
        ScheduleStatusListFilter,
        "screening_datetime",
        "fbg_datetime",
        "repeated",
        "p3_ltfu",
    ]

    search_fields = ["screening_identifier"]

    def dashboard(self, obj=None, label=None) -> str:
        url = self.get_subject_dashboard_url(obj=obj)
        if not url:
            url = reverse(
                "meta_screening_admin:meta_screening_subjectscreening_change",
                args=(obj.original_id,),
            )
        context = dict(title=_("Go to subject screening"), url=url, label=label)
        return render_to_string("dashboard_button.html", context=context)
