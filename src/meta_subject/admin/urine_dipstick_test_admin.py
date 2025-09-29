from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import UrineDipstickTestForm
from ..models import UrineDipstickTest
from .modeladmin import CrfModelAdminMixin


@admin.register(UrineDipstickTest, site=meta_subject_admin)
class UrineDipstickTestAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    form = UrineDipstickTestForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "performed",
                    "not_performed_reason",
                    "ketones",
                    "protein",
                    "glucose",
                )
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "performed": admin.VERTICAL,
        "ketones": admin.VERTICAL,
        "protein": admin.VERTICAL,
        "glucose": admin.VERTICAL,
    }
