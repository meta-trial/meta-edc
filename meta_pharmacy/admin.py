from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.list_filters import ReportDateListFilter
from edc_pharmacy.admin.list_filters import MedicationsListFilter
from edc_sites.admin import SiteModelAdminMixin

from .admin_site import meta_pharmacy_admin
from .forms import RxForm, SubstitutionsForm
from .models import Rx, Substitutions


@admin.register(Substitutions, site=meta_pharmacy_admin)
class SubstitutionsAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    """Admin class for meta_pharmacy.Substitutions"""

    form = SubstitutionsForm

    autocomplete_fields = ["rx"]

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

    radio_fields = {"arm_match": admin.VERTICAL}

    list_filter = ("arm_match", ReportDateListFilter)

    search_fields = ["subject_identifier", "sid", "dispensed_sid"]

    @admin.display(description="Report date", ordering="report_datetime")
    def report_date(self, obj) -> str | None:
        if obj.report_datetime:
            return obj.report_datetime.date()
        return None


@admin.register(Rx, site=meta_pharmacy_admin)
class RxAdmin(ModelAdminSubjectDashboardMixin, admin.ModelAdmin):
    """Admin class for proxy model of edc_pharmacy.Rx"""

    show_object_tools = True

    form = RxForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "report_datetime",
                    "rx_name",
                    "rx_date",
                    "medications",
                    "clinician_initials",
                    "notes",
                )
            },
        ),
        (
            "Randomization",
            {
                "fields": ("rando_sid", "randomizer_name", "weight_in_kgs"),
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = ("medications",)

    list_display = (
        "subject_identifier",
        "dashboard",
        "rx_medications",
        "rando_sid",
        "rx_date",
        "weight_in_kgs",
        "rx_name",
    )

    list_filter = ("report_datetime", MedicationsListFilter, "site")

    search_fields = (
        "id",
        "subject_identifier",
        "rando_sid",
        "registered_subject__initials",
        "medications__name",
        "site__id",
        "rx_name",
    )

    readonly_fields = (
        "rando_sid",
        "weight_in_kgs",
        "rx_name",
    )

    @admin.display
    def rx_medications(self, obj):
        return ", ".join([obj.display_name for obj in obj.medications.all()])
