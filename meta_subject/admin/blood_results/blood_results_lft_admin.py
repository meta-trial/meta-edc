from django.contrib import admin
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsLftForm
from ...models import BloodResultsLft
from ..modeladmin import CrfModelAdmin


@admin.register(BloodResultsLft, site=meta_subject_admin)
class BloodResultsLftAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsLftForm
    fieldsets = BloodResultFieldset(
        BloodResultsLft.lab_panel, model_cls=BloodResultsLft
    ).fieldsets
