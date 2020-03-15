from django.contrib import admin

from edc_model_admin import audit_fieldset_tuple

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsLftForm
from ...models import BloodResultsLft
from .blood_results_modeladmin_mixin import (
    BloodResultsModelAdminMixin,
    conclusion_fieldset,
    summary_fieldset,
)


@admin.register(BloodResultsLft, site=meta_subject_admin)
class BloodResultsLftAdmin(BloodResultsModelAdminMixin):

    form = BloodResultsLftForm

    autocomplete_fields = ["lft_requisition"]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Liver Function Tests", {"fields": ["lft_requisition", "lft_assay_datetime"]}),
        ("AST", {"fields": ["ast", "ast_units", "ast_abnormal", "ast_reportable"]}),
        ("ALT", {"fields": ["alt", "alt_units", "alt_abnormal", "alt_reportable"]}),
        ("ALP", {"fields": ["alp", "alp_units", "alp_abnormal", "alp_reportable"]}),
        (
            "Serum Amylase",
            {
                "fields": [
                    "amylase",
                    "amylase_units",
                    "amylase_abnormal",
                    "amylase_reportable",
                ]
            },
        ),
        ("GGT", {"fields": ["ggt", "ggt_units", "ggt_abnormal", "ggt_reportable"]}),
        (
            "Serum Albumin",
            {
                "fields": [
                    "albumin",
                    "albumin_units",
                    "albumin_abnormal",
                    "albumin_reportable",
                ]
            },
        ),
        conclusion_fieldset,
        summary_fieldset,
        audit_fieldset_tuple,
    )
