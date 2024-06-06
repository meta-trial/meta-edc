from django.contrib import admin
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from ...admin_site import meta_reports_admin
from ...models import UnattendedThreeInRow


@admin.register(UnattendedThreeInRow, site=meta_reports_admin)
class UnattendedThreeInRowAdmin(
    SiteModelAdminMixin, ModelAdminDashboardMixin, TemplatesModelAdminMixin, admin.ModelAdmin
):
    list_display = [
        "dashboard",
        "subject_identifier",
        "first",
        "second",
        "third",
        "interval_days",
        "from_now_days",
        "site",
        "created",
    ]

    list_filter = ["first", "second", "third"]

    search_fields = ["subject_identifier", "first", "second", "third"]
