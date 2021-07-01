from django.contrib import admin
from edc_blood_results.admin import BloodResultsModelAdminMixin
from edc_blood_results.fieldsets import BloodResultPanel
from edc_lab_panel.panels import lipids_panel

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsLipidForm
from ...models import BloodResultsLipid
from ..modeladmin import CrfModelAdmin


@admin.register(BloodResultsLipid, site=meta_subject_admin)
class BloodResultsLipidAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsLipidForm
    fieldsets = BloodResultPanel(lipids_panel, model_cls=BloodResultsLipid).fieldsets
