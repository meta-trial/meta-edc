from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_adverse_event.modeladmin_mixins import DeathReportModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import meta_ae_admin
from ..forms import DeathReportForm
from ..models import DeathReport


@admin.register(DeathReport, site=meta_ae_admin)
class DeathReportAdmin(DeathReportModelAdminMixin, SimpleHistoryAdmin):

    form = DeathReportForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "report_datetime",
                    "death_datetime",
                    "death_as_inpatient",
                )
            },
        ),
        (
            "Opinion of Local Study Doctor",
            {"fields": ("cause_of_death", "cause_of_death_other", "narrative")},
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )
