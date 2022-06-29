from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset

from ..admin_site import meta_subject_admin
from ..forms import ConcomitantMedicationForm
from ..models import ConcomitantMedication
from .modeladmin import CrfModelAdmin


@admin.register(ConcomitantMedication, site=meta_subject_admin)
class ConcomitantMedicationAdmin(CrfModelAdmin):

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
