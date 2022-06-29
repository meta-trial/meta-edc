from django.contrib import admin
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsLipidForm
from ...models import BloodResultsLipid
from ..modeladmin import CrfModelAdmin


@admin.register(BloodResultsLipid, site=meta_subject_admin)
class BloodResultsLipidAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsLipidForm
    fieldsets = BloodResultFieldset(
        BloodResultsLipid.lab_panel, model_cls=BloodResultsLipid
    ).fieldsets
