from __future__ import annotations

from decimal import Decimal

from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.contrib.messages import ERROR, SUCCESS
from django.core.exceptions import ObjectDoesNotExist
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin
from edc_offstudy.exceptions import OffstudyError
from edc_pharmacy.exceptions import NextStudyMedicationError, RefillCreatorError
from edc_pharmacy.model_mixins.study_medication_crf_model_mixin import (
    StudyMedicationError,
)
from edc_pharmacy.models import DosageGuideline, Formulation, Medication
from edc_utils.date import to_local
from edc_visit_schedule.utils import is_baseline

from meta_pharmacy.constants import METFORMIN

from ..admin_site import meta_subject_admin
from ..forms import StudyMedicationForm
from ..models import StudyMedication
from .list_filters import RefillEndDateListFilter, RefillStartDateListFilter
from .modeladmin import CrfModelAdminMixin


@admin.register(StudyMedication, site=meta_subject_admin)
class StudyMedicationAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    actions = ("create_or_update_rx_refills",)

    form = StudyMedicationForm

    autocomplete_fields = (
        "dosage_guideline",
        "formulation",
    )

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
        (
            "Dispensed medication",
            {
                "description": (
                    "Type in the stock code on the medication "
                    "bottle or bottles. Separate by comma."
                ),
                "fields": ("stock_codes",),
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "formulation": admin.VERTICAL,
        "refill": admin.VERTICAL,
        "refill_to_next_visit": admin.VERTICAL,
    }

    def get_list_filter(self, request) -> tuple[str | type[SimpleListFilter], ...]:
        list_filter = super().get_list_filter(request)
        list_filter = list(list_filter)
        list_filter.insert(4, "dosage_guideline")
        list_filter.insert(4, RefillEndDateListFilter)
        list_filter.insert(4, RefillStartDateListFilter)
        return tuple(list_filter)

    def get_list_display(self, request) -> tuple[str, ...]:
        list_display = super().get_list_display(request)
        list_display = list(list_display)
        list_display.insert(4, "refill_days")
        list_display.insert(4, "refill_end_date")
        list_display.insert(4, "refill_start_date")
        list_display.insert(4, "dosage_guideline")
        return tuple(list_display)

    @admin.display(description="days", ordering="number_of_days")
    def refill_days(self, obj):
        return obj.number_of_days

    @admin.display(description="refill_start", ordering="refill_start_datetime")
    def refill_start_date(self, obj):
        if obj.refill_start_datetime:
            return to_local(obj.refill_start_datetime).date()
        return None

    @admin.display(description="refill_end", ordering="refill_end_datetime")
    def refill_end_date(self, obj):
        if obj.refill_end_datetime:
            return to_local(obj.refill_end_datetime).date()
        return None

    @admin.action(permissions=["view"], description="Create or update RX Refills")
    def create_or_update_rx_refills(self, request, queryset):
        updated = 0
        errors = 0
        medication = Medication.objects.get(name=METFORMIN)
        formulation = Formulation.objects.get(medication=medication, strength=500)
        dosage_guideline_baseline = DosageGuideline.objects.get(
            medication=medication, dose=Decimal("1000.0")
        )
        dosage_guideline_followup = DosageGuideline.objects.get(
            medication=medication, dose=Decimal("2000.0")
        )
        for obj in queryset:
            obj.refill_identifier = obj.id
            if not obj.formulation:
                obj.formulation = formulation
            if not obj.dosage_guideline:
                if is_baseline(obj.related_visit):
                    obj.dosage_guideline = dosage_guideline_baseline
                else:
                    obj.dosage_guideline = dosage_guideline_followup
            updated, errors = self.rx_refills_save_or_raise(request, obj, updated, errors)
        messages.add_message(
            request, SUCCESS, f"Updated {updated} documents with {errors} errors."
        )

    @staticmethod
    def rx_refills_save_or_raise(request, obj, updated, errors):
        try:
            obj.save()
        except NextStudyMedicationError as e:
            messages.add_message(request, ERROR, f"NextStudyMedicationError: {e}")
            errors += 1
        except ObjectDoesNotExist as e:
            messages.add_message(
                request,
                ERROR,
                (f"ObjectDoesNotExist: {obj.subject_identifier}, {obj.related_visit}, {e!s}"),
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
        return updated, errors
