from django.contrib import admin
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsLipidsForm
from ...models import BloodResultsLipids
from ..modeladmin import CrfModelAdminMixin


@admin.register(BloodResultsLipids, site=meta_subject_admin)
class BloodResultsLipidsAdmin(
    BloodResultsModelAdminMixin, CrfModelAdminMixin, SimpleHistoryAdmin
):
    form = BloodResultsLipidsForm
    fieldsets = BloodResultFieldset(
        BloodResultsLipids.lab_panel,
        model_cls=BloodResultsLipids,
        extra_fieldsets=[
            (-1, action_fieldset_tuple),
        ],
    ).fieldsets
