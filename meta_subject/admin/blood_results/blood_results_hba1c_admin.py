from django.contrib import admin

from edc_model_admin import audit_fieldset_tuple

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsHba1cForm
from ...models import BloodResultsHba1c
from .blood_results_modeladmin_mixin import BloodResultsModelAdminMixin


@admin.register(BloodResultsHba1c, site=meta_subject_admin)
class BloodResultsHba1cAdmin(BloodResultsModelAdminMixin):

    form = BloodResultsHba1cForm

    autocomplete_fields = ["hba1c_requisition"]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "HbA1c",
            {
                "fields": [
                    "is_poc",
                    "hba1c_requisition",
                    "hba1c_assay_datetime",
                    "hba1c",
                    "hba1c_units",
                    # "hba1c_abnormal",
                    # "hba1c_reportable",
                ]
            },
        ),
        # conclusion_fieldset,
        # summary_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "is_poc": admin.VERTICAL,
        "results_abnormal": admin.VERTICAL,
        "results_reportable": admin.VERTICAL,
    }
