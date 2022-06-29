from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset

from ..admin_site import meta_subject_admin
from ..forms import UrinePregnancyForm
from ..models import UrinePregnancy
from .modeladmin import CrfModelAdmin


@admin.register(UrinePregnancy, site=meta_subject_admin)
class UrinePregnancyAdmin(CrfModelAdmin):

    form = UrinePregnancyForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "performed",
                    "not_performed_reason",
                    "assay_date",
                    "bhcg_value",
                )
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "performed": admin.VERTICAL,
        "bhcg_value": admin.VERTICAL,
    }
