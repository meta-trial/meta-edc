from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import GlucoseForm
from ..models import Glucose
from .modeladmin import CrfModelAdmin


@admin.register(Glucose, site=meta_subject_admin)
class GlucoseAdmin(CrfModelAdmin):

    form = GlucoseForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Fasting",
            {
                "fields": (
                    "fasting",
                    "fasting_duration_str",
                )
            },
        ),
        (
            "IFG",
            {
                "fields": (
                    "ifg_performed",
                    "ifg_not_performed_reason",
                    "ifg_datetime",
                    "ifg_value",
                    "ifg_units",
                )
            },
        ),
        (
            "OGTT",
            {
                "fields": (
                    "ogtt_performed",
                    "ogtt_not_performed_reason",
                    "ogtt_base_datetime",
                    "ogtt_datetime",
                    "ogtt_value",
                    "ogtt_units",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "fasting": admin.VERTICAL,
        "ifg_units": admin.VERTICAL,
        "ifg_performed": admin.VERTICAL,
        "ogtt_performed": admin.VERTICAL,
        "ogtt_units": admin.VERTICAL,
    }
