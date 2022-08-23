from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import ActionItemModelAdminMixin, action_fieldset_tuple
from edc_data_manager.modeladmin_mixins import DataManagerModelAdminMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_prn_admin
from ..forms import LossToFollowupForm
from ..models import LossToFollowup


@admin.register(LossToFollowup, site=meta_prn_admin)
class LossToFollowupAdmin(
    DataManagerModelAdminMixin,
    ActionItemModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):

    form = LossToFollowupForm

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        (
            "Loss to followup",
            {
                "fields": (
                    "last_seen_datetime",
                    "number_consecutive_missed_visits",
                    "last_missed_visit_datetime",
                    "home_visited",
                    "home_visit_detail",
                    "loss_category",
                    "loss_category_other",
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
        "last_seen_datetime",
        "number_consecutive_missed_visits",
        "home_visited",
    )

    list_filter = (
        "last_seen_datetime",
        "last_missed_visit_datetime",
        "number_consecutive_missed_visits",
    )

    radio_fields = {
        "home_visited": admin.VERTICAL,
        "loss_category": admin.VERTICAL,
    }
