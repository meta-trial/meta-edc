from copy import copy

from django.contrib import admin
from edc_action_item import action_fields, action_fieldset_tuple
from edc_model_admin import audit_fieldset_tuple

from meta_ae.models import DeathReport

from ...models import LossToFollowup


class EndOfStudyAdminMixin:

    form = None

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
                    "offstudy_datetime",
                    "offstudy_reason",
                    "other_offstudy_reason",
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
        "offstudy_datetime",
        "tracking_identifier",
        "action_identifier",
    )

    list_filter = ("offstudy_datetime",)

    radio_fields = {"offstudy_reason": admin.VERTICAL}

    search_fields = ("subject_identifier", "action_identifier", "tracking_identifier")

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        fields = list(action_flds) + list(fields)
        return fields
