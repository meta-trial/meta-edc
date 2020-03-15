from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import UrineDipstickTestForm
from ..models import UrineDipstickTest
from .modeladmin import CrfModelAdmin


@admin.register(UrineDipstickTest, site=meta_subject_admin)
class UrineDipstickTestAdmin(CrfModelAdmin):

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
        audit_fieldset_tuple,
    )

    radio_fields = {
        "performed": admin.VERTICAL,
        "ketones": admin.VERTICAL,
        "protein": admin.VERTICAL,
        "glucose": admin.VERTICAL,
    }
