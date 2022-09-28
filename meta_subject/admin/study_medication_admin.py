from django.contrib import admin, messages
from django.contrib.messages import ERROR, SUCCESS
from django.core.exceptions import ObjectDoesNotExist
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_offstudy.exceptions import OffstudyError
from edc_pharmacy.exceptions import NextStudyMedicationError, RefillCreatorError
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
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "refill",
                )
            },
        ),
        (
            "Details",
            {
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
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "formulation": admin.VERTICAL,
        "refill": admin.VERTICAL,
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
            except NextStudyMedicationError as e:
                messages.add_message(request, ERROR, f"NextStudyMedicationError: {e}")
                errors += 1
            except ObjectDoesNotExist as e:
                messages.add_message(
                    request,
                    ERROR,
                    (
                        f"ObjectDoesNotExist: {obj.subject_identifier}, "
                        f"{obj.related_visit}, {str(e)}"
                    ),
                )
                errors += 1
            except StudyMedicationError as e:
                messages.add_message(request, ERROR, f"StudyMedicationError: {e}")
                errors += 1
            except RefillCreatorError as e:
                messages.add_message(request, ERROR, f"RefillCreatorError: {e}")
                errors += 1
            except OffstudyError as e:
                messages.add_message(request, ERROR, f"OffstudyError: {e}")
                errors += 1
            else:
                updated += 1
        messages.add_message(
            request, SUCCESS, f"Updated {updated} documents with {errors} errors."
        )
