from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import HepatitisTestForm
from ..models import HepatitisTest
from .modeladmin import CrfModelAdminMixin


@admin.register(HepatitisTest, site=meta_subject_admin)
class HepatitisTestAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
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

    radio_fields = {  # noqa: RUF012
        "hbsag_performed": admin.VERTICAL,
        "hbsag": admin.VERTICAL,
        "hcv_performed": admin.VERTICAL,
        "hcv": admin.VERTICAL,
    }
