from copy import copy

from django.contrib import admin
from edc_action_item import action_fields, action_fieldset_tuple
from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin, audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from meta_subject.models import UrinePregnancy

from ..admin_site import meta_prn_admin
from ..forms import PregnancyNotificationForm
from ..models import PregnancyNotification


@admin.register(PregnancyNotification, site=meta_prn_admin)
class PregnancyNotificationAdmin(
    DataManagerModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
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

    list_display = (
        "subject_identifier",
        "dashboard",
        "edd",
        "may_contact",
    )

    list_filter = ("edd", "may_contact")

    radio_fields = {
        "bhcg_confirmed": admin.VERTICAL,
        "may_contact": admin.VERTICAL,
    }

    search_fields = ("subject_identifier", "action_identifier", "tracking_identifier")

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        action_flds.remove("action_identifier")
        fields = list(action_flds) + list(fields)
        return fields
