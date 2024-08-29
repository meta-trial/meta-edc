from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_qareports.modeladmin_mixins import NoteModelAdminMixin

from ....admin_site import meta_reports_admin
from ....forms import MissingOgttNoteForm
from ....models import MissingOgttNote


@admin.register(MissingOgttNote, site=meta_reports_admin)
class MissingOgttNoteModelAdmin(
    NoteModelAdminMixin,
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

    radio_fields = {
        "ogtt_units": admin.VERTICAL,
        "result_status": admin.VERTICAL,
        "fasting": admin.VERTICAL,
    }
