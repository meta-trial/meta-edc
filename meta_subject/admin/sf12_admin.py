from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin
from edc_qol.admin import sf12_fieldsets, sf12_radio_fields

from ..admin_site import meta_subject_admin
from ..forms import Sf12Form
from ..models import Sf12
from .modeladmin import CrfModelAdminMixin


@admin.register(Sf12, site=meta_subject_admin)
class Sf12Admin(CrfModelAdminMixin, SimpleHistoryAdmin):
    form = Sf12Form

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        *sf12_fieldsets(),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = sf12_radio_fields()
