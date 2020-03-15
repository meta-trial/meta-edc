from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import MalariaTestForm
from ..models import MalariaTest
from .modeladmin import CrfModelAdmin


@admin.register(MalariaTest, site=meta_subject_admin)
class MalariaTestAdmin(CrfModelAdmin):

    form = MalariaTestForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "performed",
                    "diagnostic_type",
                    "not_performed_reason",
                    "result",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "performed": admin.VERTICAL,
        "diagnostic_type": admin.VERTICAL,
        "result": admin.VERTICAL,
    }
