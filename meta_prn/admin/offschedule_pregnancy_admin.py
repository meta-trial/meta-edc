from django.contrib import admin
from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import meta_prn_admin
from ..models import OffSchedulePregnancy


@admin.register(OffSchedulePregnancy, site=meta_prn_admin)
class OffSchedulePregnancyAdmin(
    DataManagerModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    instructions = None

    fields = ("subject_identifier", "offschedule_datetime")

    list_display = ("subject_identifier", "dashboard", "offschedule_datetime")

    list_filter = ("offschedule_datetime",)

    def get_readonly_fields(self, request, obj=None):
        return ["subject_identifier", "offschedule_datetime"]
