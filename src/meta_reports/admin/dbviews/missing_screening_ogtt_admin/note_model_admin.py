from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from ....admin_site import meta_reports_admin
from ....forms import MissingOgttNoteForm
from ....models import MissingOgttNote


@admin.register(MissingOgttNote, site=meta_reports_admin)
class MissingOgttNoteModelAdmin(
    SiteModelAdminMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    """A modeladmin class for the Note model."""

    form = MissingOgttNoteForm
    note_template_name = "edc_qareports/qa_report_note.html"

    fieldsets = (
        (
            None,
            {"fields": ("subject_identifier", "report_datetime", "result_status")},
        ),
        (
            "OGTT",
            {
                "fields": (
                    "fasting",
                    "ogtt_base_datetime",
                    "ogtt_datetime",
                    "ogtt_value",
                    "ogtt_units",
                )
            },
        ),
        (
            "Note",
            {
                "fields": (
                    "note",
                    "report_model",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "ogtt_units": admin.VERTICAL,
        "result_status": admin.VERTICAL,
        "fasting": admin.VERTICAL,
    }

    list_display = (
        "subject_identifier",
        "note",
        "status",
        "report_datetime",
    )

    # radio_fields = {"status": admin.VERTICAL}

    list_filter = (
        "report_datetime",
        "status",
        "report_model",
        "user_created",
        "user_modified",
    )

    search_fields = ("subject_identifier", "name")

    def get_view_only_site_ids_for_user(self, request) -> list[int]:
        return [s.id for s in request.user.userprofile.sites.all() if s.id != request.site.id]
