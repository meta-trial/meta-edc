from django.contrib import admin
from edc_blood_results.admin import BloodResultsModelAdminMixin
from edc_blood_results.fieldsets import BloodResultFieldset

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsRftForm
from ...models import BloodResultsRft
from ..modeladmin import CrfModelAdmin


@admin.register(BloodResultsRft, site=meta_subject_admin)
class BloodResultsRftAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsRftForm
    fieldsets = (
        *BloodResultFieldset(
            BloodResultsRft.lab_panel,
            model_cls=BloodResultsRft,
            excluded_utest_ids=["egfr"],
        ).fieldsets,
        (
            "Calculated eGFR",
            {"classes": ("collapse",), "fields": ["egfr_value", "egfr_units"]},
        ),
    )

    readonly_fields = ["egfr_value", "egfr_units"]
