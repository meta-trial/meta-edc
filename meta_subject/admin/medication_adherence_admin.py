from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_adherence.model_admin_mixin import (
    MedicationAdherenceAdminMixin,
    get_visual_score_fieldset_tuple,
    missed_medications_fieldset_tuple,
)

from ..admin_site import meta_subject_admin
from ..forms import MedicationAdherenceForm
from ..models import MedicationAdherence
from .modeladmin import CrfModelAdmin

pill_count_fieldset_tuple = (
    "Pill Count",
    {
        "fields": ["pill_count_performed", "pill_count_not_performed_reason", "pill_count"],
    },
)


@admin.register(MedicationAdherence, site=meta_subject_admin)
class MedicationAdherenceAdmin(MedicationAdherenceAdminMixin, CrfModelAdmin):

    form = MedicationAdherenceForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        get_visual_score_fieldset_tuple(),
        pill_count_fieldset_tuple,
        missed_medications_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "pill_count_performed": admin.VERTICAL,
        "last_missed_pill": admin.VERTICAL,
    }
