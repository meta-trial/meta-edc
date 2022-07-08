from dateutil.relativedelta import relativedelta
from django.contrib import admin
from edc_action_item import action_fieldset_tuple
from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin, audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from meta_consent.models import SubjectConsent

from ..admin_site import meta_prn_admin
from ..forms import EndOfStudyForm
from ..models import EndOfStudy


@admin.register(EndOfStudy, site=meta_prn_admin)
class EndOfStudyAdmin(
    DataManagerModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):

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

    radio_fields = {
        "offstudy_reason": admin.VERTICAL,
        "clinical_withdrawal_reason": admin.VERTICAL,
        "toxicity_withdrawal_reason": admin.VERTICAL,
    }

    search_fields = ["subject_identifier"]

    list_filter = ["offstudy_reason", "last_seen_date"]

    list_display = [
        "subject_identifier",
        "terminated",
        "last_seen",
        "months",
        "reason",
    ]

    @admin.display(description="terminated", ordering="offstudy_datetime")
    def terminated(self, obj):
        return obj.offstudy_datetime.date()

    @admin.display(description="last_seen", ordering="last_seen_date")
    def last_seen(self, obj):
        return obj.last_seen_date

    @admin.display(description="reason", ordering="offstudy_reason")
    def reason(self, obj):
        return obj.offstudy_reason

    @admin.display(description="months")
    def months(self, obj):
        subject_consent = SubjectConsent.objects.get(subject_identifier=obj.subject_identifier)
        return relativedelta(obj.offstudy_datetime, subject_consent.consent_datetime).months
