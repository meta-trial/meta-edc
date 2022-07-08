from copy import copy

from django.contrib import admin
from edc_action_item import action_fields, action_fieldset_tuple
from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin, audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import meta_prn_admin
from ..forms import OffstudyMedicationForm
from ..models import OffstudyMedication


@admin.register(OffstudyMedication, site=meta_prn_admin)
class OffstudyMedicationAdmin(
    DataManagerModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
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

    list_display = (
        "subject_identifier",
        "dashboard",
        "stop_date",
        "last_dose_date",
    )

    list_filter = (
        "reason",
        "stop_date",
        "last_dose_date",
    )

    radio_fields = {
        "reason": admin.VERTICAL,
    }

    search_fields = ("subject_identifier", "action_identifier", "tracking_identifier")

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        action_flds.remove("action_identifier")
        fields = list(action_flds) + list(fields)
        return fields
