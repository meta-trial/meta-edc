from django.contrib import admin
from django.urls import reverse
from django_audit_fields import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import meta_spfq_admin
from ..forms import SpfqRefusalForm
from ..models import SpfqRefusal


@admin.register(SpfqRefusal, site=meta_spfq_admin)
class SpfqRefusalAdmin(
    ModelAdminSubjectDashboardMixin,
    SiteModelAdminMixin,
    SimpleHistoryAdmin,
):
    ordering = ("-created",)

    form = SpfqRefusalForm

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        (
            "Contact effort",
            {
                "fields": (
                    "contact_attempted",
                    "contact_attempts_count",
                    "contact_made",
                    "contact_attempts_explained",
                ),
            },
        ),
        (
            "Reason not consenting",
            {
                "fields": ("reason",),
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "contact_attempted": admin.VERTICAL,
        "contact_made": admin.VERTICAL,
    }

    list_display = (
        "subject_identifier",
        "dashboard",
        "report_datetime",
        "contact_attempted",
        "contact_attempts_count",
        "contact_made",
    )

    search_fields = ("subject_identifier",)

    def get_post_url_on_delete(self, request, obj) -> str | None:  # noqa: ARG002
        return reverse("meta_spfq_admin:meta_spfq_spfqlist_changelist")
