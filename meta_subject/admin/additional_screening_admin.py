from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import AdditionalScreeningForm
from ..models import AdditionalScreening
from .modeladmin import CrfModelAdmin


@admin.register(AdditionalScreening, site=meta_subject_admin)
class AdditionalScreeningAdmin(CrfModelAdmin):

    form = AdditionalScreeningForm

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
        audit_fieldset_tuple,
    )
