from copy import copy

from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields import audit_fieldset_tuple
from edc_action_item import action_fields, action_fieldset_tuple
from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import meta_prn_admin
from ..forms import OffScheduleForm
from ..models import EndOfStudy, OffSchedule


@admin.register(OffSchedule, site=meta_prn_admin)
class OffScheduleAdmin(
    DataManagerModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = OffScheduleForm

    additional_instructions = format_html(
        '<span style="color:orange;font-weight:bold">Note:</span> Detailed '
        "information about study termination will be asked for on the "
        f"<b>{EndOfStudy._meta.verbose_name}</b> form"
    )

    fieldsets = (
        (None, {"fields": ("subject_identifier", "offschedule_datetime")}),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    list_display = ("subject_identifier", "dashboard", "offschedule_datetime")

    list_filter = ("offschedule_datetime",)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        fields = list(action_flds) + list(fields)
        return fields
