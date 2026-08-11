from clinicedc_constants import NOT_APPLICABLE
from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.admin.list_filters import SiteListFilter

from ..admin_site import meta_ae_admin
from ..forms import AeFinalClassificationForm
from ..models import AeFinalClassification
from .list_filters import FinalAeClassificationSetListFilter, HasAeTmgListFilter


@admin.register(AeFinalClassification, site=meta_ae_admin)
class AeFinalClassificationAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = AeFinalClassificationForm
    show_object_tools = True
    change_list_note = "You may only edit documents from the current site."

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "report_datetime",
                ),
            },
        ),
        (
            "Final AE Classification",
            {
                "fields": (
                    "final_ae_classification",
                    "final_ae_classification_other",
                    "verified",
                ),
            },
        ),
        (
            "Original AE Report",
            {
                "description": "Copied from the original AE report (read-only).",
                "fields": (
                    "ae_initial",
                    "ae_initial_action_identifier",
                    "ae_classification",
                    "ae_classification_other",
                ),
            },
        ),
        (
            "AE TMG Report",
            {
                "description": "Copied from the AE TMG (read-only).",
                "fields": (
                    "ae_tmg",
                    "ae_tmg_action_identifier",
                    "investigator_ae_classification_agreed",
                    "investigator_ae_classification",
                    "investigator_ae_classification_other",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "final_ae_classification": admin.VERTICAL,
        "ae_classification": admin.VERTICAL,
        "investigator_ae_classification": admin.VERTICAL,
        "investigator_ae_classification_agreed": admin.VERTICAL,
    }

    list_display = (
        "subject_identifier",
        "dashboard",
        "report_datetime",
        "final",
        "original",
        "tmg",
        "agreed",
    )

    list_filter = (
        FinalAeClassificationSetListFilter,
        "verified",
        HasAeTmgListFilter,
        "investigator_ae_classification_agreed",
        SiteListFilter,
        "final_ae_classification",
    )

    search_fields = (
        "subject_identifier",
        "ae_initial_action_identifier",
        "ae_tmg_action_identifier",
    )

    readonly_fields = (
        "subject_identifier",
        "ae_initial",
        "ae_initial_action_identifier",
        "ae_classification",
        "ae_classification_other",
        "ae_tmg",
        "ae_tmg_action_identifier",
        "investigator_ae_classification_agreed",
        "investigator_ae_classification",
        "investigator_ae_classification_other",
    )

    @admin.display(description="Final")
    def final(self, obj=None):
        return obj.final_ae_classification

    @admin.display(description="AE")
    def original(self, obj=None):
        return obj.ae_classification

    @admin.display(description="TMG")
    def tmg(self, obj=None):
        if (
            obj.investigator_ae_classification
            and obj.investigator_ae_classification.name == NOT_APPLICABLE
        ):
            return None
        return obj.investigator_ae_classification

    @admin.display(description="TMG agreed")
    def agreed(self, obj=None):
        return obj.investigator_ae_classification_agreed

    def get_view_only_site_ids_for_user(self, request) -> list[int]:
        return [s.id for s in request.user.userprofile.sites.all() if s.id != request.site.id]

    def user_may_view_other_sites(self, request) -> bool:  # noqa: ARG002
        return True
