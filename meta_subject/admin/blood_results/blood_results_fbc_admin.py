from django.contrib import admin

from edc_model_admin import audit_fieldset_tuple

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsFbcForm
from ...models import BloodResultsFbc
from .blood_results_modeladmin_mixin import (
    BloodResultsModelAdminMixin,
    conclusion_fieldset,
    summary_fieldset,
)


@admin.register(BloodResultsFbc, site=meta_subject_admin)
class BloodResultsFbcAdmin(BloodResultsModelAdminMixin):

    form = BloodResultsFbcForm

    autocomplete_fields = ["fbc_requisition"]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("FBC", {"fields": ["fbc_requisition", "fbc_assay_datetime"]}),
        (
            "Haemoglobin",
            {
                "fields": [
                    "haemoglobin",
                    "haemoglobin_units",
                    "haemoglobin_abnormal",
                    "haemoglobin_reportable",
                ]
            },
        ),
        ("HCT", {"fields": ["hct", "hct_units", "hct_abnormal", "hct_reportable"]}),
        ("RBC", {"fields": ["rbc", "rbc_units", "rbc_abnormal", "rbc_reportable"]}),
        ("WBC", {"fields": ["wbc", "wbc_units", "wbc_abnormal", "wbc_reportable"]}),
        (
            "Platelets",
            {
                "fields": [
                    "platelets",
                    "platelets_units",
                    "platelets_abnormal",
                    "platelets_reportable",
                ]
            },
        ),
        conclusion_fieldset,
        summary_fieldset,
        audit_fieldset_tuple,
    )
