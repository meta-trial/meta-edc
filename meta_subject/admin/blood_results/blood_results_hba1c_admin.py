from django.contrib import admin
from edc_blood_results.admin import BloodResultsModelAdminMixin
from edc_blood_results.fieldsets import BloodResultFieldset
from edc_lab_panel.panels import hba1c_panel

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsHba1cForm
from ...models import BloodResultsHba1c
from ..modeladmin import CrfModelAdmin

# TODO: add is poc?


@admin.register(BloodResultsHba1c, site=meta_subject_admin)
class BloodResultsHba1cAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsHba1cForm
    fieldsets = BloodResultFieldset(hba1c_panel).fieldsets
