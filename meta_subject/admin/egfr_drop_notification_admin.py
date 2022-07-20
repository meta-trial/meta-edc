from copy import copy

from django.contrib import admin
from edc_action_item import (
    ActionItemModelAdminMixin,
    action_fields,
    action_fieldset_tuple,
)
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

    list_display = (
        "report_datetime",
        "report_status",
        "creatinine_date",
        "egfr_percent_change",
    )

    list_filter = ("site", "report_status", "report_datetime", "creatinine_date")

    radio_fields = {"report_status": admin.VERTICAL}

    search_fields = (
        "subject_visit__subject_identifier",
        "action_identifier",
        "tracking_identifier",
    )

    readonly_fields = [
        "creatinine_date",
        "egfr_percent_change",
    ]

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        action_flds.remove("action_identifier")
        fields = list(action_flds) + list(fields)
        return fields
