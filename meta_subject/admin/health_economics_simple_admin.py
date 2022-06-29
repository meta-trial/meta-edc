from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_he import education_fieldset, education_radio_fields

from ..admin_site import meta_subject_admin
from ..forms import HealthEconomicsSimpleForm
from ..models import HealthEconomicsSimple
from .modeladmin import CrfModelAdmin


@admin.register(HealthEconomicsSimple, site=meta_subject_admin)
class HealthEconomicsSimpleAdmin(CrfModelAdmin):

    form = HealthEconomicsSimpleForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "marital_status",
                    "occupation",
                )
            },
        ),
        education_fieldset,
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {**education_radio_fields}
