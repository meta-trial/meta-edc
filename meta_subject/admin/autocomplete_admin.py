from django.contrib import admin
from edc_list_data.admin import ListModelAdminMixin
from edc_pharmacy.admin import DosageGuidelineAdmin as BaseDosageGuidelineAdmin
from edc_pharmacy.admin import FormulationAdmin as BaseFormulationAdmin
from edc_pharmacy.admin import MedicationAdmin as BaseMedicationAdmin
from edc_pharmacy.models import DosageGuideline, Formulation, Medication

from meta_lists.models import ArvRegimens

from ..admin_site import meta_subject_admin


@admin.register(ArvRegimens, site=meta_subject_admin)
class ArvRegimensAdmin(ListModelAdminMixin, admin.ModelAdmin):
    """Registered again for the autocomplete field"""

    pass


@admin.register(DosageGuideline, site=meta_subject_admin)
class DosageGuidelineAdmin(BaseDosageGuidelineAdmin):
    """Registered again for the autocomplete field"""

    pass


@admin.register(Medication, site=meta_subject_admin)
class MedicationAdmin(BaseMedicationAdmin):
    """Registered again for the autocomplete field"""

    pass


@admin.register(Formulation, site=meta_subject_admin)
class FormulationAdmin(BaseFormulationAdmin):
    """Registered again for the autocomplete field"""

    pass
