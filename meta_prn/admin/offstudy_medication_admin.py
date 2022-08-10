from typing import Tuple

from django.contrib import admin
from edc_action_item import ActionItemModelAdminMixin, action_fieldset_tuple
from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin, audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import meta_prn_admin
from ..forms import OffstudyMedicationForm
from ..models import OffstudyMedication


@admin.register(OffstudyMedication, site=meta_prn_admin)
class OffstudyMedicationAdmin(
    DataManagerModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = OffstudyMedicationForm

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        (
            "Loss to followup",
            {
                "fields": (
                    "stop_date",
                    "last_dose_date",
                    "reason",
                    "reason_other",
                    "comment",
                )
            },
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "reason": admin.VERTICAL,
    }

    def get_list_display(self, request) -> Tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = (
            "subject_identifier",
            "dashboard",
            "stop_date",
            "last_dose_date",
        )
        return custom_fields + tuple(f for f in list_display if f not in custom_fields)

    def get_list_filter(self, request) -> Tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = (
            "reason",
            "stop_date",
            "last_dose_date",
        )
        return custom_fields + tuple(f for f in list_filter if f not in custom_fields)

    def get_search_fields(self, request) -> Tuple[str, ...]:
        custom_fields = ("subject_identifier", "action_identifier", "tracking_identifier")
        return tuple(set(super().get_search_fields(request) + custom_fields))
