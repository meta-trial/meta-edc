from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.fieldsets import visit_schedule_fieldset_tuple
from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from ..admin_site import meta_subject_admin
from ..forms import SubjectVisitForm
from ..models import SubjectVisit
from .modeladmin import ModelAdminMixin


@admin.register(SubjectVisit, site=meta_subject_admin)
class SubjectVisitAdmin(
    VisitModelAdminMixin, SiteModelAdminMixin, ModelAdminMixin, SimpleHistoryAdmin
):
    show_dashboard_in_list_display_pos = 2

    form = SubjectVisitForm

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "appointment",
                    "report_datetime",
                    "reason",
                    "reason_unscheduled",
                    "reason_unscheduled_other",
                    "info_source",
                    "info_source_other",
                    "comments",
                ]
            },
        ),
        visit_schedule_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "reason": admin.VERTICAL,
        "reason_unscheduled": admin.VERTICAL,
        "info_source": admin.VERTICAL,
    }
