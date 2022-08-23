from typing import Tuple

from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_action_item import ActionItemModelAdminMixin, action_fieldset_tuple
from edc_data_manager.modeladmin_mixins import DataManagerModelAdminMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

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

    def get_list_display(self, request) -> Tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = ("subject_identifier", "dashboard", "offschedule_datetime")
        return custom_fields + tuple(f for f in list_display if f not in custom_fields)

    def get_list_filter(self, request) -> Tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = ("offschedule_datetime",)
        return custom_fields + tuple(f for f in list_filter if f not in custom_fields)

    def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
        custom_fields = ("subject_identifier", "offschedule_datetime")
        return tuple(set(super().get_readonly_fields(request, obj=obj) + custom_fields))
