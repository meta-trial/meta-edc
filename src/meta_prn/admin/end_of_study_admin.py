from clinicedc_constants import OTHER
from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_action_item.modeladmin_mixins import ActionItemModelAdminMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from meta_ae.models import DeathReport
from meta_consent.models import SubjectConsent
from meta_lists.models import OffstudyReasons

from ..admin_site import meta_prn_admin
from ..forms import EndOfStudyForm
from ..models import EndOfStudy, LossToFollowup


@admin.register(EndOfStudy, site=meta_prn_admin)
class EndOfStudyAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):
    additional_instructions = format_html(
        "{html}",
        html=mark_safe(  # noqa: S308
            render_to_string(
                "meta_prn/eos/additional_instructions.html",
                context=dict(
                    death_report=DeathReport._meta.verbose_name,
                    ltfu=LossToFollowup._meta.verbose_name,
                ),
            )
        ),  # nosec #B703 # B308
    )

    form = EndOfStudyForm

    date_hierarchy = "offstudy_datetime"

    fieldsets = (
        [
            None,
            {
                "fields": (
                    "subject_identifier",
                    "offstudy_datetime",
                    "last_seen_date",
                )
            },
        ],
        [
            "Off-study reason",
            {
                "fields": (
                    "offstudy_reason",
                    "other_offstudy_reason",
                )
            },
        ],
        [
            "Dates from supporting documents (if applicable)",
            {
                "fields": (
                    "death_date",
                    "ltfu_date",
                    "transfer_date",
                    "pregnancy_date",
                    "delivery_date",
                )
            },
        ],
        [
            "Toxicity (if applicable)",
            {
                "description": (
                    "This section is applicable if the patient experienced an "
                    "unacceptable toxicity, as indicated above"
                ),
                "fields": (
                    "toxicity_withdrawal_reason",
                    "toxicity_withdrawal_reason_other",
                ),
            },
        ],
        [
            "Withdrawn on CLINICAL grounds (if applicable)",
            {
                "description": (
                    "This section is applicable if the patient was withdrawn "
                    "on clinical grounds, as indicated above"
                ),
                "fields": (
                    "clinical_withdrawal_reason",
                    "clinical_withdrawal_investigator_decision",
                    "clinical_withdrawal_reason_other",
                ),
            },
        ],
        [
            "Comment",
            {"fields": ("comment",)},
        ],
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "offstudy_reason": admin.VERTICAL,
        "clinical_withdrawal_reason": admin.VERTICAL,
        "toxicity_withdrawal_reason": admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "offstudy_reason":
            kwargs["queryset"] = OffstudyReasons.objects.order_by("display_index")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_list_display(self, request) -> tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = (
            "subject_identifier",
            "dashboard",
            "terminated",
            "last_seen",
            "months",
            "reason",
        )
        return custom_fields + tuple(
            f for f in list_display if f not in (*custom_fields, "__str__")
        )

    def get_list_filter(self, request) -> tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = ("offstudy_reason", "last_seen_date")
        return custom_fields + tuple(f for f in list_filter if f not in custom_fields)

    def get_search_fields(self, request) -> tuple[str, ...]:
        search_fields = super().get_search_fields(request)
        custom_fields = ("subject_identifier",)
        return tuple(set(custom_fields + search_fields))

    @admin.display(description="terminated", ordering="offstudy_datetime")
    def terminated(self, obj):
        return obj.offstudy_datetime.date()

    @admin.display(description="last_seen", ordering="last_seen_date")
    def last_seen(self, obj):
        return obj.last_seen_date

    @admin.display(description="Offstudy reason", ordering="offstudy_reason")
    def reason(self, obj):
        return (
            obj.offstudy_reason if obj.offstudy_reason != OTHER else obj.other_offstudy_reason
        )

    @admin.display(description="M")
    def months(self, obj):
        subject_consent = SubjectConsent.objects.get(subject_identifier=obj.subject_identifier)
        return relativedelta(obj.offstudy_datetime, subject_consent.consent_datetime).months
