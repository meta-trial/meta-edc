from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import StudyMedicationForm
from ..models import StudyMedication
from .modeladmin import CrfModelAdmin


@admin.register(StudyMedication, site=meta_subject_admin)
class StudyMedicationAdmin(CrfModelAdmin):

    form = StudyMedicationForm

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
        audit_fieldset_tuple,
    )
