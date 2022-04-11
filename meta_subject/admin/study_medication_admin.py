from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import StudyMedicationForm
from ..models import StudyMedication
from .modeladmin import CrfModelAdmin


@admin.register(StudyMedication, site=meta_subject_admin)
class StudyMedicationAdmin(CrfModelAdmin):

    form = StudyMedicationForm

    autocomplete_fields = [
        "dosage_guideline",
        "formulation",
        "next_dosage_guideline",
        "next_formulation",
    ]

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
        (
            "This refill",
            {
                "fields": (
                    "dosage_guideline",
                    "formulation",
                    "number_of_days",
                    "special_instructions",
                )
            },
        ),
        (
            "Next refill",
            {
                "fields": (
                    "order_next",
                    "next_dosage_guideline",
                    "next_formulation",
                )
            },
        ),
        # refill_fieldset_tuple
        audit_fieldset_tuple,
    )

    radio_fields = {
        "formulation": admin.VERTICAL,
        "next_dosage_guideline": admin.VERTICAL,
        "next_formulation": admin.VERTICAL,
        "order_next": admin.VERTICAL,
    }
