from django.contrib import admin
from django.template.loader import render_to_string

from ..admin_site import meta_reports_admin
from ..models import Endpoints
from .modeladmin_mixins import EndpointsModelAdminMixin


@admin.register(Endpoints, site=meta_reports_admin)
class EndpointsAdmin(EndpointsModelAdminMixin, admin.ModelAdmin):
    queryset_filter = dict(referral_date__isnull=True, offstudy_date__isnull=True)  # noqa: RUF012

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
        "last_updated",
    )

    def rendered_change_list_note(self):
        return render_to_string("meta_reports/endpoints_change_list_note.html")
