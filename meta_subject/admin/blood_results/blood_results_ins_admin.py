from django.contrib import admin
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsInsForm
from ...models import BloodResultsIns
from ..modeladmin import CrfModelAdmin


@admin.register(BloodResultsIns, site=meta_subject_admin)
class BloodResultsInsAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsInsForm
    fieldsets = BloodResultFieldset(
        BloodResultsIns.lab_panel, model_cls=BloodResultsIns
    ).fieldsets
