from django.contrib import admin
from edc_action_item import ActionItemModelAdminMixin, action_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin, audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import EgfrDropNotificationForm
from ..models import EgfrDropNotification
from .modeladmin import CrfModelAdminMixin


@admin.register(EgfrDropNotification, site=meta_subject_admin)
class EgfrDropNotificationAdmin(
    DataManagerModelAdminMixin,
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = EgfrDropNotificationForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "eGFR",
            {
                "fields": (
                    "creatinine_date",
                    "egfr_percent_change",
                )
            },
        ),
        (
            "Narrative",
            {"fields": ("narrative", "report_status")},
        ),
        crf_status_fieldset,
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {"report_status": admin.VERTICAL}

    search_fields = (
        "subject_visit__subject_identifier",
        "action_identifier",
        "tracking_identifier",
    )

    def get_readonly_fields(self, request, obj=None) -> tuple:
        fields = super().get_readonly_fields(request, obj)
        fields = ("creatinine_date", "egfr_percent_change") + fields
        return tuple(fields)

    def get_list_filter(self, request) -> tuple:
        list_filter = super().get_list_filter(request)
        list_filter = ("report_status", "creatinine_date") + list_filter
        return list_filter

    def get_list_display(self, request) -> tuple:
        list_display = super().get_list_display(request)
        egfr_fields = [
            "report_datetime",
            "report_status",
            "creatinine_date",
            "egfr_percent_change",
            "created",
            "modified",
        ]
        list_display = [f for f in list_display if f not in egfr_fields] + egfr_fields
        return tuple(list_display)
