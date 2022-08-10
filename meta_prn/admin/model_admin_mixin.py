from typing import Tuple

from django.contrib import admin
from django.utils.html import format_html
from edc_action_item import action_fieldset_tuple
from edc_model_admin import audit_fieldset_tuple

from meta_ae.models import DeathReport

from ..models import LossToFollowup


class EndOfStudyAdminMixin:

    form = None

    additional_instructions = format_html(
        "Note: if the patient is <i>deceased</i>, complete form "
        "`{}` before completing this form. "
        "<BR>If the patient is </i>lost to follow up</i>, complete form "
        "`{}` before completing this form.",
        DeathReport._meta.verbose_name,
        LossToFollowup._meta.verbose_name,
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

    radio_fields = {"offstudy_reason": admin.VERTICAL}

    search_fields = ("subject_identifier", "action_identifier", "tracking_identifier")

    def get_list_display(self, request) -> Tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = (
            "subject_identifier",
            "dashboard",
            "offstudy_datetime",
            "tracking_identifier",
            "action_identifier",
        )
        return custom_fields + tuple(f for f in list_display if f not in custom_fields)

    def get_list_filter(self, request) -> Tuple[str, ...]:
        list_filter = super().get_list_display(request)
        custom_fields = ("offstudy_datetime",)
        return custom_fields + tuple(f for f in list_filter if f not in custom_fields)
