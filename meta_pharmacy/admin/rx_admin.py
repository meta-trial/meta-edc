from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_pharmacy.admin.list_filters import MedicationsListFilter

from ..admin_site import meta_pharmacy_admin
from ..forms import RxForm
from ..models import Rx


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
        "rx_expiration_date",
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
