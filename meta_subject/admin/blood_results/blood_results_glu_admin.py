from django.contrib import admin

from edc_model_admin import audit_fieldset_tuple

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsGluForm
from ...models import BloodResultsGlu
from .blood_results_modeladmin_mixin import (
    BloodResultsModelAdminMixin,
    conclusion_fieldset,
    summary_fieldset,
)


@admin.register(BloodResultsGlu, site=meta_subject_admin)
class BloodResultsGluAdmin(BloodResultsModelAdminMixin):

    form = BloodResultsGluForm

    autocomplete_fields = ["glucose_requisition"]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Blood Glucose",
            {
                "fields": [
                    "is_poc",
                    "glucose_requisition",
                    "glucose_assay_datetime",
                    "fasting",
                    "glucose",
                    "glucose_units",
                    "glucose_abnormal",
                    "glucose_reportable",
                ]
            },
        ),
        conclusion_fieldset,
        summary_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "is_poc": admin.VERTICAL,
        "fasting": admin.VERTICAL,
        "results_abnormal": admin.VERTICAL,
        "results_reportable": admin.VERTICAL,
    }
