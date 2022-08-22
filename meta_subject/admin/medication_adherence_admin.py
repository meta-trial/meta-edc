from django.contrib import admin
from edc_adherence.model_admin_mixin import MedicationAdherenceAdminMixin

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
