from django.contrib import admin

from edc_model_admin import audit_fieldset_tuple

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsRftForm
from ...models import BloodResultsRft
from .blood_results_modeladmin_mixin import (
    BloodResultsModelAdminMixin,
    conclusion_fieldset,
    summary_fieldset,
)


@admin.register(BloodResultsRft, site=meta_subject_admin)
class BloodResultsRftAdmin(BloodResultsModelAdminMixin):

    form = BloodResultsRftForm

    autocomplete_fields = ["rft_requisition"]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Renal Function Tests", {"fields": ["rft_requisition", "rft_assay_datetime"]}),
        (
            "Serum Urea",
            {"fields": ["urea", "urea_units", "urea_abnormal", "urea_reportable"]},
        ),
        (
            "Serum Creatinine",
            {
                "fields": [
                    "creatinine",
                    "creatinine_units",
                    "creatinine_abnormal",
                    "creatinine_reportable",
                ]
            },
        ),
        (
            "Serum Uric Acid",
            {
                "fields": [
                    "uric_acid",
                    "uric_acid_units",
                    "uric_acid_abnormal",
                    "uric_acid_reportable",
                ]
            },
        ),
        ("eGFR (Calculated)", {"fields": ["egfr"]}),
        conclusion_fieldset,
        summary_fieldset,
        audit_fieldset_tuple,
    )

    readonly_fields = ["egfr"]
