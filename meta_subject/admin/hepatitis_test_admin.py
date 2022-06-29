from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset

from ..admin_site import meta_subject_admin
from ..forms import HepatitisTestForm
from ..models import HepatitisTest
from .modeladmin import CrfModelAdmin


@admin.register(HepatitisTest, site=meta_subject_admin)
class HepatitisTestAdmin(CrfModelAdmin):

    form = HepatitisTestForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                )
            },
        ),
        (
            "Hepatitis B",
            {
                "fields": (
                    "hbsag_performed",
                    "hbsag",
                    "hbsag_date",
                )
            },
        ),
        (
            "Hepatitis C",
            {
                "fields": (
                    "hcv_performed",
                    "hcv",
                    "hcv_date",
                )
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "hbsag_performed": admin.VERTICAL,
        "hbsag": admin.VERTICAL,
        "hcv_performed": admin.VERTICAL,
        "hcv": admin.VERTICAL,
    }
