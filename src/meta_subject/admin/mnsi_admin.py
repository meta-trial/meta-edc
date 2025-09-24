from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_mnsi.admin_site import edc_mnsi_admin
from edc_mnsi.fieldsets import calculated_values_fieldset
from edc_mnsi.fieldsets import get_fieldsets as get_mnsi_fieldsets
from edc_mnsi.model_admin_mixin import MnsiModelAdminMixin, radio_fields
from edc_mnsi.models import Mnsi as DefaultMnsi
from edc_model_admin.history import SimpleHistoryAdmin

from meta_subject.admin_site import meta_subject_admin

from ..forms import MnsiForm
from ..models import Mnsi
from .modeladmin import CrfModelAdminMixin


def get_fieldsets():
    fieldset = (
        None,
        {
            "fields": (
                "subject_visit",
                "report_datetime",
                "mnsi_performed",
                "mnsi_not_performed_reason",
            )
        },
    )

    return (
        fieldset,
        *get_mnsi_fieldsets(),
        crf_status_fieldset_tuple,
        calculated_values_fieldset,
        audit_fieldset_tuple,
    )


edc_mnsi_admin.unregister(DefaultMnsi)
radio_fields.update(crf_status=admin.VERTICAL)


@admin.register(Mnsi, site=meta_subject_admin)
class MnsiAdmin(
    MnsiModelAdminMixin,
    CrfModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = MnsiForm

    fieldsets = get_fieldsets()

    radio_fields = radio_fields
