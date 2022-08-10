from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_action_item import ActionItemModelAdminMixin, action_fieldset_tuple
from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import meta_prn_admin
from ..models import OffSchedulePostnatal


@admin.register(OffSchedulePostnatal, site=meta_prn_admin)
class OffSchedulePostnatalAdmin(
    DataManagerModelAdminMixin,
    ActionItemModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):

    instructions = None

    fieldsets = (
        (None, {"fields": ("subject_identifier", "offschedule_datetime")}),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    list_display = ("subject_identifier", "dashboard", "offschedule_datetime")

    list_filter = ("offschedule_datetime",)

    readonly_fields = ["subject_identifier", "offschedule_datetime"]
