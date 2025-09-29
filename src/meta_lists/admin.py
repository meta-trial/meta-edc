from django.contrib import admin
from edc_list_data.admin import ListModelAdminMixin

from .admin_site import meta_lists_admin
from .models import (
    ArvRegimens,
    BaselineSymptoms,
    Complications,
    DiabetesSymptoms,
    DmMedications,
    DmTreatments,
    HealthcareWorkers,
    Investigations,
    NonAdherenceReasons,
    OffstudyReasons,
    OiProphylaxis,
    SubjectVisitMissedReasons,
    Symptoms,
)


@admin.register(SubjectVisitMissedReasons, site=meta_lists_admin)
class SubjectVisitMissedReasonsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Symptoms, site=meta_lists_admin)
class SymptomsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ArvRegimens, site=meta_lists_admin)
class ArvRegimensAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(OffstudyReasons, site=meta_lists_admin)
class OffstudyReasonsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(OiProphylaxis, site=meta_lists_admin)
class OiProphylaxisAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(BaselineSymptoms, site=meta_lists_admin)
class BaselineSymptomsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(DiabetesSymptoms, site=meta_lists_admin)
class DiabetesSymptomsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(NonAdherenceReasons, site=meta_lists_admin)
class NonAdherenceReasonsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(DmMedications, site=meta_lists_admin)
class DmMedicationsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(DmTreatments, site=meta_lists_admin)
class DmTreatmentsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Complications, site=meta_lists_admin)
class ComplicationsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Investigations, site=meta_lists_admin)
class InvestigationsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(HealthcareWorkers, site=meta_lists_admin)
class HealthcareWorkersAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass
