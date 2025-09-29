from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.list_filters import ReportDateListFilter
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import meta_pharmacy_admin
from ..forms import SubstitutionsForm
from ..models import Substitutions


@admin.register(Substitutions, site=meta_pharmacy_admin)
class SubstitutionsAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    """Admin class for meta_pharmacy.Substitutions"""

    form = SubstitutionsForm

    autocomplete_fields = ("rx",)

    add_instructions = "This form is used to record any substitions made for IMP refills"

    fieldsets = (
        (
            None,
            {"fields": ("report_datetime",)},
        ),
        ("Original label on bottle", {"fields": ("sid", "visit_no")}),
        (
            "Substitution / Changed label",
            {
                "description": "The label on this bottle has been changed to the following",
                "fields": ("dispensed_sid", "updated_visit_no"),
            },
        ),
        (
            "Subject",
            {
                "fields": ("rx",),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "sid",
        "dispensed_sid",
        "arm_match",
        "subject_identifier",
        "report_date",
    )

    radio_fields = {"arm_match": admin.VERTICAL}  # noqa: RUF012

    list_filter = ("arm_match", ReportDateListFilter)

    search_fields = ("subject_identifier", "sid", "dispensed_sid")

    @admin.display(description="Report date", ordering="report_datetime")
    def report_date(self, obj) -> str | None:
        if obj.report_datetime:
            return obj.report_datetime.date()
        return None
