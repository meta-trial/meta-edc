from typing import Tuple

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import ActionItemModelAdminMixin, action_fieldset_tuple
from edc_data_manager.modeladmin_mixins import DataManagerModelAdminMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_prn_admin
from ..forms import OffStudyMedicationForm
from ..models import OffStudyMedication


@admin.register(OffStudyMedication, site=meta_prn_admin)
class OffStudyMedicationAdmin(
    DataManagerModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = OffStudyMedicationForm

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        (
            "Loss to followup",
            {
                "fields": (
                    "medications",
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

    filter_horizontal = ("medications",)

    search_fields = ("subject_identifier",)

    def get_list_display(self, request) -> Tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = (
            "subject_identifier",
            "dashboard",
            "decision_date",
            "last_known_dose_date",
        )
        return custom_fields + tuple(f for f in list_display if f not in custom_fields)

    def get_list_filter(self, request) -> Tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = (
            "medications",
            "reason",
            "stop_date",
            "last_dose_date",
        )
        return custom_fields + tuple(f for f in list_filter if f not in custom_fields)

    @admin.display(description="decision date", ordering="stop_date")
    def decision_date(self, obj=None):
        return obj.stop_date

    @admin.display(description="last dose date", ordering="last_dose_date")
    def last_known_dose_date(self, obj=None):
        return obj.last_dose_date
