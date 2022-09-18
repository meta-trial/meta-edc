from django.contrib import admin, messages
from django.contrib.messages import ERROR, SUCCESS
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_pharmacy.model_mixins.study_medication_crf_model_mixin import (
    StudyMedicationError,
)

from ..admin_site import meta_subject_admin
from ..forms import StudyMedicationForm
from ..models import StudyMedication
from .modeladmin import CrfModelAdmin


@admin.register(StudyMedication, site=meta_subject_admin)
class StudyMedicationAdmin(CrfModelAdmin):

    actions = ["create_or_update_rx_refills"]

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
                "description": "This refill will be dispensed at this visit",
                "fields": (
                    "refill_start_datetime",
                    "dosage_guideline",
                    "formulation",
                    "refill_to_next_visit",
                    "refill_end_datetime",
                    "special_instructions",
                ),
            },
        ),
        (
            "Next refill",
            {
                "description": "This refill will be dispensed at the next scheduled visit",
                "fields": (
                    "order_or_update_next",
                    "next_dosage_guideline",
                    "next_formulation",
                ),
            },
        ),
        # refill_fieldset_tuple
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "formulation": admin.VERTICAL,
        "next_dosage_guideline": admin.VERTICAL,
        "next_formulation": admin.VERTICAL,
        "order_or_update_next": admin.VERTICAL,
        "refill_to_next_visit": admin.VERTICAL,
    }

    @admin.action(permissions=["view"], description="Create or update RX Refills")
    def create_or_update_rx_refills(self, request, queryset):
        updated = 0
        errors = 0
        for obj in StudyMedication.objects.filter(site_id=request.site.id).order_by(
            "modified"
        ):
            try:
                obj.save()
            except StudyMedicationError:
                messages.add_message(request, ERROR, f"Failed to update document. See {obj}.")
                errors += 1
            else:
                updated += 1
        messages.add_message(
            request, SUCCESS, f"Updated {updated} documents with {errors} errors."
        )
