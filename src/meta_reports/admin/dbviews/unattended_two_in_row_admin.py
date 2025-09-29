from django.contrib import admin
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ...admin_site import meta_reports_admin
from ...models import UnattendedTwoInRow


@admin.register(UnattendedTwoInRow, site=meta_reports_admin)
class UnattendedTwoInRowAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    ordering = ("site", "subject_identifier")
    list_display = (
        "dashboard",
        "subject_identifier",
        "first_value",
        "second_value",
        "interval_days",
        "from_now_days",
        "site",
        "created",
    )

    list_filter = (ScheduleStatusListFilter, "first_value", "second_value")

    search_fields = ("subject_identifier", "first_value", "second_value")
