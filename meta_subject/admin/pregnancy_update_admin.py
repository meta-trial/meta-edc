from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset

from ..admin_site import meta_subject_admin
from ..forms import PregnancyUpdateForm
from ..models import PregnancyUpdate
from .modeladmin import CrfModelAdmin


@admin.register(PregnancyUpdate, site=meta_subject_admin)
class PregnancyUpdateAdmin(CrfModelAdmin):

    form = PregnancyUpdateForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Update",
            {
                "fields": (
                    "contact",
                    "comment",
                )
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "contact": admin.VERTICAL,
    }
