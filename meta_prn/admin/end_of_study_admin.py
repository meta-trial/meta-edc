from copy import copy

from django.contrib import admin
from edc_action_item import action_fields, action_fieldset_tuple
from edc_model_admin import SimpleHistoryAdmin, audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from meta_ae.models import DeathReport

from ..admin_site import meta_prn_admin
from ..forms import EndOfStudyForm
from ..models import EndOfStudy, LossToFollowup


@admin.register(EndOfStudy, site=meta_prn_admin)
class EndOfStudyAdmin(ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin):

    form = EndOfStudyForm

    additional_instructions = (
        "Note: if the patient is <i>deceased</i>, complete form "
        f"`{DeathReport._meta.verbose_name}` before completing this form. "
        "<BR>If the patient is </i>lost to follow up</i>, complete form "
        f"`{LossToFollowup._meta.verbose_name}` before completing this form."
    )

    fieldsets = (
        [
            "Part 1:",
            {
                "fields": (
                    "subject_identifier",
                    "offschedule_datetime",
                    "offschedule_reason",
                    "other_offschedule_reason",
                    "ltfu_date",
                    "death_date",
                    "comment",
                )
            },
        ],
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    list_display = (
        "subject_identifier",
        "dashboard",
        "offschedule_datetime",
        "tracking_identifier",
        "action_identifier",
    )

    list_filter = ("offschedule_datetime",)

    radio_fields = {"offschedule_reason": admin.VERTICAL}

    search_fields = ("subject_identifier", "action_identifier", "tracking_identifier")

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        fields = list(action_flds) + list(fields)
        return fields
