from django.contrib import admin
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsFbcForm
from ...models import BloodResultsFbc
from ..modeladmin import CrfModelAdmin


@admin.register(BloodResultsFbc, site=meta_subject_admin)
class BloodResultsFbcAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsFbcForm
    fieldsets = BloodResultFieldset(
        BloodResultsFbc.lab_panel, model_cls=BloodResultsFbc
    ).fieldsets
