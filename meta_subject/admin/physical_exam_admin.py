from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import PhysicalExamForm
from ..models import PhysicalExam
from .modeladmin import CrfModelAdmin


@admin.register(PhysicalExam, site=meta_subject_admin)
class PhysicalExamAdmin(CrfModelAdmin):

    form = PhysicalExamForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Part 1: BP and Heart",
            {
                "fields": (
                    "sys_blood_pressure",
                    "dia_blood_pressure",
                    "heart_rate",
                    "irregular_heartbeat",
                    "irregular_heartbeat_description",
                    "respiratory_rate",
                )
            },
        ),
        (
            "Part 2: Other vitals",
            {"fields": ("temperature", "weight", "waist_circumference")},
        ),
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
    }
