from django.contrib import admin
from django.utils.safestring import mark_safe
from django_audit_fields.admin import audit_fieldset_tuple, ModelAdminAuditFieldsMixin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_action_item.modeladmin_mixins import ModelAdminActionItemMixin
from edc_model_admin import (
    ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminInstitutionMixin,
    TemplatesModelAdminMixin,
)
from edc_model_admin.model_admin_simple_history import SimpleHistoryAdmin
from edc_notification.modeladmin_mixins import NotificationModelAdminMixin

from ..admin_site import meta_screening_admin
from ..models import IcpReferral


@admin.register(IcpReferral, site=meta_screening_admin)
class IcpReferralAdmin(
    TemplatesModelAdminMixin,
    NotificationModelAdminMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,
    ModelAdminAuditFieldsMixin,
    ModelAdminInstitutionMixin,
    ModelAdminActionItemMixin,
    SimpleHistoryAdmin,
):

    # form =

    additional_instructions = (
        "Subject was referred after not meeting META trial eligibility criteria."
    )

    fieldsets = (
        [
            None,
            {
                "fields": (
                    "report_datetime",
                    "screening_identifier",
                    "hospital_identifier",
                    "meta_eligible",
                    "meta_eligibility_datetime",
                )
            },
        ],
        [
            "Criteria",
            {
                "fields": (
                    "gender",
                    "initials",
                    "age_in_years",
                    "ethnicity",
                    "hiv_pos",
                    "art_six_months",
                    "fasting_glucose",
                    "hba1c",
                    "ogtt_two_hr",
                )
            },
        ],
        ["Referral Reasons", {"fields": ("referral_reasons",)}],
        audit_fieldset_tuple,
    )

    list_display = (
        "screening_identifier",
        "report_datetime",
        "criteria",
        "demographics",
        "user_created",
        "created",
    )

    list_filter = ("report_datetime", "meta_eligibility_datetime", "gender")

    search_fields = ("screening_identifier", "hospital_identifier", "initials")

    readonly_fields = (
        "screening_identifier",
        "hospital_identifier",
        "report_datetime",
        "gender",
        "initials",
        "age_in_years",
        "ethnicity",
        "hiv_pos",
        "art_six_months",
        "fasting_glucose",
        "hba1c",
        "ogtt_two_hr",
        "meta_eligible",
        "meta_eligibility_datetime",
        "referral_reasons",
    )

    def demographics(self, obj=None):
        return mark_safe(
            f"{obj.get_gender_display()} {obj.age_in_years}yrs<BR>"
            f"Initials: {obj.initials.upper()}<BR><BR>"
            f"Hospital ID: {obj.hospital_identifier}"
        )

    def criteria(self, obj):
        if obj.referral_reasons:
            return mark_safe("<BR>".join(obj.referral_reasons.split("|")))
        return None
