from django.contrib import admin
from edc_action_item import action_fieldset_tuple
from edc_lab_panel.panels import hba1c_panel
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsHba1cForm
from ...models import BloodResultsHba1c
from ..modeladmin import CrfModelAdmin

# TODO: add is poc? YES, always


@admin.register(BloodResultsHba1c, site=meta_subject_admin)
class BloodResultsHba1cAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsHba1cForm
    fieldsets = BloodResultFieldset(
        hba1c_panel,
        extra_fieldsets=[
            (-1, action_fieldset_tuple),
        ],
    ).fieldsets
