from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_adverse_event.modeladmin_mixins import DeathReportModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import meta_ae_admin
from ..forms import DeathReportForm
from ..models import DeathReport


@admin.register(DeathReport, site=meta_ae_admin)
class DeathReportAdmin(SiteModelAdminMixin, DeathReportModelAdminMixin, SimpleHistoryAdmin):
    form = DeathReportForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "report_datetime",
                    "death_datetime",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "death_as_inpatient",
                    "death_location",
                    "hospital_name",
                )
            },
        ),
        (
            "Informant Information",
            {
                "fields": (
                    "informant_contact",
                    "informant_relationship",
                    "other_informant_relationship",
                )
            },
        ),
        (
            "Cause of death",
            {
                "description": (
                    "If death occurred in hospital or a death certificate is available, "
                    "please indicate the recorded causes of death"
                ),
                "fields": (
                    "cause_of_death",
                    "cause_of_death_other",
                    "secondary_cause_of_death",
                    "secondary_cause_of_death_other",
                    "narrative",
                ),
            },
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "cause_of_death": admin.VERTICAL,
        "death_as_inpatient": admin.VERTICAL,
        "death_location": admin.VERTICAL,
        "informant_relationship": admin.VERTICAL,
        "secondary_cause_of_death": admin.VERTICAL,
    }
