from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from meta_edc.meta_version import get_meta_version

from ..admin_site import meta_subject_admin
from ..forms import PhysicalExamForm
from ..models import PhysicalExam
from .fields import get_blood_pressure_fields
from .modeladmin import CrfModelAdmin


def get_other_vitals_fieldset():
    fields = ["temperature"]
    if get_meta_version() == 2:
        fields.extend(["weight", "waist_circumference"])
    return (
        "Part 2: Other vitals",
        {"fields": tuple(fields)},
    )


@admin.register(PhysicalExam, site=meta_subject_admin)
class PhysicalExamAdmin(CrfModelAdmin):

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
        audit_fieldset_tuple,
    )

    radio_fields = {
        "abdominal_tenderness": admin.VERTICAL,
        "enlarged_liver": admin.VERTICAL,
        "irregular_heartbeat": admin.VERTICAL,
        "jaundice": admin.VERTICAL,
        "peripheral_oedema": admin.VERTICAL,
        "severe_htn": admin.VERTICAL,
    }
