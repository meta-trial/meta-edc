from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import PhysicalExamForm
from ..models import PhysicalExam
from .fields import get_blood_pressure_fields
from .modeladmin import CrfModelAdminMixin


def get_other_vitals_fieldset():
    return (
        "Part 2: Other vitals",
        {"fields": ["temperature", "waist_circumference"]},
    )


@admin.register(PhysicalExam, site=meta_subject_admin)
class PhysicalExamAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    form = PhysicalExamForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Part 1: BP and Heart",
            {
                "fields": (
                    *get_blood_pressure_fields(),
                    "heart_rate",
                    "irregular_heartbeat",
                    "irregular_heartbeat_description",
                    "respiratory_rate",
                )
            },
        ),
        get_other_vitals_fieldset(),
        (
            "Part 3: Signs",
            {
                "fields": (
                    "jaundice",
                    "peripheral_oedema",
                    "abdominal_tenderness",
                    "abdominal_tenderness_description",
                    "enlarged_liver",
                )
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "abdominal_tenderness": admin.VERTICAL,
        "enlarged_liver": admin.VERTICAL,
        "irregular_heartbeat": admin.VERTICAL,
        "jaundice": admin.VERTICAL,
        "peripheral_oedema": admin.VERTICAL,
        "severe_htn": admin.VERTICAL,
    }
