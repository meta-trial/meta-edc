from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import (
    NoteStatusListFilter as BaseNoteStatusListFilter,
)
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ....admin_site import meta_reports_admin
from ....models import NOTE_STATUSES, MissingScreeningOgtt


class NoteStatusListFilter(BaseNoteStatusListFilter):
    note_model_status_choices = NOTE_STATUSES


@admin.register(MissingScreeningOgtt, site=meta_reports_admin)
class MissingScreeningOgttAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    note_model = "meta_reports.missingogttnote"
    note_status_list_filter = NoteStatusListFilter
    note_template = "edc_qareports/columns/notes_column.html"
    include_note_column = True

    ordering = ("site", "subject_identifier")

    list_display = (
        "dashboard",
        "subject_identifier",
        "site",
        "screening_date",
        "fbg_date",
        "fbg_value",
        "ogtt_value",
        "repeated",
        "p3_ltfu",
        "fbg2_value",
        "ogtt2_value",
        "fbg2_datetime",
        "ogtt2_datetime",
        "consented",
    )

    list_filter = (
        ScheduleStatusListFilter,
        "screening_datetime",
        "fbg_datetime",
        "repeated",
        "p3_ltfu",
    )

    search_fields = ("subject_identifier",)

    def dashboard(self, obj=None, label=None) -> str:
        url = self.get_subject_dashboard_url(obj=obj)
        if not url:
            url = reverse(
                "meta_screening_admin:meta_screening_subjectscreening_change",
                args=(obj.original_id,),
            )
        context = dict(title=_("Go to subject screening"), url=url, label=label)
        return render_to_string("edc_subject_dashboard/dashboard_button.html", context=context)

    @admin.display(description="Screen date", ordering="screening_datetime")
    def screening_date(self, obj):
        if obj.screening_datetime:
            return obj.screening_datetime.date()
        return None

    @admin.display(description="Fbg date", ordering="fbg_datetime")
    def fbg_date(self, obj):
        if obj.fbg_datetime:
            return obj.fbg_datetime.date()
        return None
