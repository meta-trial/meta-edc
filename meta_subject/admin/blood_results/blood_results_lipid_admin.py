from django.contrib import admin

from edc_model_admin import audit_fieldset_tuple

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsLipidForm
from ...models import BloodResultsLipid
from .blood_results_modeladmin_mixin import (
    BloodResultsModelAdminMixin,
    conclusion_fieldset,
    summary_fieldset,
)


@admin.register(BloodResultsLipid, site=meta_subject_admin)
class BloodResultsLipidAdmin(BloodResultsModelAdminMixin):

    form = BloodResultsLipidForm

    autocomplete_fields = ["lipid_requisition"]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Lipid Tests", {"fields": ["lipid_requisition", "lipid_assay_datetime"]}),
        ("LDL", {"fields": ["ldl", "ldl_units", "ldl_abnormal", "ldl_reportable"]}),
        ("HDL", {"fields": ["hdl", "hdl_units", "hdl_abnormal", "hdl_reportable"]}),
        (
            "Triglycerides",
            {"fields": ["trig", "trig_units", "trig_abnormal", "trig_reportable"]},
        ),
        conclusion_fieldset,
        summary_fieldset,
        audit_fieldset_tuple,
    )
