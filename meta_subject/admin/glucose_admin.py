from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset

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
            "FBG",
            {
                "fields": (
                    "fbg_performed",
                    "fbg_not_performed_reason",
                    "fbg_datetime",
                    "fbg_value",
                    "fbg_units",
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
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "fasting": admin.VERTICAL,
        "fbg_units": admin.VERTICAL,
        "fbg_performed": admin.VERTICAL,
        "ogtt_performed": admin.VERTICAL,
        "ogtt_units": admin.VERTICAL,
    }
