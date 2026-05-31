from django.contrib import admin
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_crf.fieldset import crf_status_not_collapsed_fieldset
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsLftForm
from ...models import BloodResultsLft
from ..modeladmin import CrfModelAdminMixin


@admin.register(BloodResultsLft, site=meta_subject_admin)
class BloodResultsLftAdmin(
    BloodResultsModelAdminMixin, CrfModelAdminMixin, SimpleHistoryAdmin
):
    form = BloodResultsLftForm
    fieldsets = BloodResultFieldset(
        BloodResultsLft.lab_panel,
        model_cls=BloodResultsLft,
        extra_fieldsets=[
            (-1, action_fieldset_tuple),
            (-1, crf_status_not_collapsed_fieldset),
        ],
    ).fieldsets
