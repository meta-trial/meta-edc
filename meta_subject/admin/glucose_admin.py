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
        ("Fasting", {"fields": ("fasted", "fasted_duration_str",)},),
        (
            "IFG",
            {
                "fields": (
                    "ifg_performed",
                    "ifg_not_performed_reason",
                    "fasting_glucose_datetime",
                    "fasting_glucose",
                    "fasting_glucose_units",
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
                    "ogtt_two_hr_datetime",
                    "ogtt_two_hr",
                    "ogtt_two_hr_units",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "fasted": admin.VERTICAL,
        "fasting_glucose_units": admin.VERTICAL,
        "ifg_performed": admin.VERTICAL,
        "ogtt_performed": admin.VERTICAL,
        "ogtt_two_hr_units": admin.VERTICAL,
    }
