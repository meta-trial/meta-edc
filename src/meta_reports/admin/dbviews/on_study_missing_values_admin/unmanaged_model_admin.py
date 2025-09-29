from django.contrib import admin
from edc_qareports.modeladmin_mixins import OnStudyMissingValuesModelAdminMixin

from ....admin_site import meta_reports_admin
from ....models import OnStudyMissingValues


@admin.register(OnStudyMissingValues, site=meta_reports_admin)
class OnStudyMissingValuesAdmin(OnStudyMissingValuesModelAdminMixin, admin.ModelAdmin):
    include_note_column: bool = True
    project_reports_admin: str = "meta_reports_admin"
    project_subject_admin: str = "meta_subject_admin"
