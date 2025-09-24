from django.contrib import admin
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsInsForm
from ...models import BloodResultsIns
from ..modeladmin import CrfModelAdminMixin


@admin.register(BloodResultsIns, site=meta_subject_admin)
class BloodResultsInsAdmin(
    BloodResultsModelAdminMixin, CrfModelAdminMixin, SimpleHistoryAdmin
):
    form = BloodResultsInsForm
    fieldsets = BloodResultFieldset(
        BloodResultsIns.lab_panel,
        model_cls=BloodResultsIns,
        extra_fieldsets=[
            (-1, action_fieldset_tuple),
        ],
    ).fieldsets
