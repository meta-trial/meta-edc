from django.contrib import admin
from edc_qareports.modeladmin_mixins import OnStudyMissingValuesModelAdminMixin

from ....admin_site import meta_reports_admin
from ....models import OnStudyMissingLabValues


@admin.register(OnStudyMissingLabValues, site=meta_reports_admin)
class OnStudyMissingLabValuesAdmin(OnStudyMissingValuesModelAdminMixin, admin.ModelAdmin):
    include_note_column: bool = True
