from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import ConcomitantMedicationForm
from ..models import ConcomitantMedication
from .modeladmin import CrfModelAdminMixin


@admin.register(ConcomitantMedication, site=meta_subject_admin)
class ConcomitantMedicationAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    form = ConcomitantMedicationForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                )
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )
