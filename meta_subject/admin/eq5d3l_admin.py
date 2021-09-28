from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_qol.admin import eq5d3l_fieldsets, eq5d3l_radio_fields

from ..admin_site import meta_subject_admin
from ..forms import Eq5d3lForm
from ..models import Eq5d3l
from .modeladmin import CrfModelAdmin


@admin.register(Eq5d3l, site=meta_subject_admin)
class Eq5d3lAdmin(CrfModelAdmin):

    form = Eq5d3lForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        *eq5d3l_fieldsets(),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = eq5d3l_radio_fields()
