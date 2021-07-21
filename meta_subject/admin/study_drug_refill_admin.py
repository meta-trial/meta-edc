from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from meta_subject.models import StudyDrugRefill

from ..admin_site import meta_subject_admin
from ..forms import StudyDrugRefillForm
from .modeladmin import CrfModelAdmin


@admin.register(StudyDrugRefill, site=meta_subject_admin)
class StudyDrugRefillAdmin(CrfModelAdmin):

    form = StudyDrugRefillForm

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
