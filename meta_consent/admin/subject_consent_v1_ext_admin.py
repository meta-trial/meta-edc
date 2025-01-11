from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_consent_admin
from ..forms import SubjectConsentV1ExtForm
from ..models import SubjectConsentV1Ext


@admin.register(SubjectConsentV1Ext, site=meta_consent_admin)
class SubjectConsentV1ExtAdmin(
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentV1ExtForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_consent",
                    "report_datetime",
                    "agrees_to_extension",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {"agrees_to_extension": admin.VERTICAL}

    def get_readonly_fields(self, request, obj=None) -> tuple[str, ...]:
        if obj:
            return ("subject_consent",)
        return ()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject_consent":
            subject_identifier = request.GET.get("subject_identifier")
            kwargs["queryset"] = db_field.related_model.objects.filter(
                subject_identifier=subject_identifier
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
