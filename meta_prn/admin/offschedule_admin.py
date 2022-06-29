from django.contrib import admin
from django.utils.html import format_html
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

    fields = ("subject_identifier", "offschedule_datetime")

    list_display = ("subject_identifier", "dashboard", "offschedule_datetime")

    list_filter = ("offschedule_datetime",)
