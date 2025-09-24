from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_action_item.modeladmin_mixins import ActionItemModelAdminMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import meta_prn_admin
from ..forms import DmReferralForm
from ..models import DmReferral


@admin.register(DmReferral, site=meta_prn_admin)
class DmReferralAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = DmReferralForm

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        ("Referral to Diabetes clinic", {"fields": ("referral_date",)}),
        (
            "Diabetes diagnosis",
            {
                "fields": ("referral_note",),
            },
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    list_display = (
        "subject_identifier",
        "dashboard",
        "report_datetime",
        "referral_date_as_col",
    )

    list_filter = (
        "report_datetime",
        "referral_date",
    )

    @admin.display(description="Referral date", ordering="referral_date")
    def referral_date_as_col(self, obj=None):
        return obj.referral_date
