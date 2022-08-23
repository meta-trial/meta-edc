from typing import Tuple

from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import ActionItemModelAdminMixin, action_fieldset_tuple
from edc_data_manager.modeladmin_mixins import DataManagerModelAdminMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from meta_subject.models import UrinePregnancy

from ..admin_site import meta_prn_admin
from ..forms import PregnancyNotificationForm
from ..models import PregnancyNotification


@admin.register(PregnancyNotification, site=meta_prn_admin)
class PregnancyNotificationAdmin(
    DataManagerModelAdminMixin,
    ActionItemModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):

    form = PregnancyNotificationForm

    additional_instructions = (
        "Important: A positive Urine βhCG must be entered before this form "
        f"may be completed (See `{UrinePregnancy._meta.verbose_name}`)."
    )

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        (
            "Pregnancy",
            {"fields": ("bhcg_confirmed", "unconfirmed_details", "bhcg_date")},
        ),
        (
            "Delivery",
            {"fields": ("edd",)},
        ),
        (
            "Followup",
            {"fields": ("may_contact",)},
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "bhcg_confirmed": admin.VERTICAL,
        "may_contact": admin.VERTICAL,
    }

    def get_list_display(self, request) -> Tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = (
            "subject_identifier",
            "dashboard",
            "edd",
            "may_contact",
        )
        return custom_fields + tuple(f for f in list_display if f not in custom_fields)

    def get_list_filter(self, request) -> Tuple[str, ...]:
        list_filter = super().get_list_display(request)
        custom_fields = ("edd", "may_contact")
        return custom_fields + tuple(f for f in list_filter if f not in custom_fields)
