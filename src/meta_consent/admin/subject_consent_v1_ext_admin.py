from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_consent_admin
from ..forms import SubjectConsentV1ExtForm
from ..models import SubjectConsentV1Ext
from .list_filters import AgreesListFilter


@admin.register(SubjectConsentV1Ext, site=meta_consent_admin)
class SubjectConsentV1ExtAdmin(
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentV1ExtForm

    additional_instructions = (
        "This consent offers the participant the option to agree to "
        "extend clinic followup from the original 36 months to 48 months. "
    )

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
        (
            "Review Questions",
            {
                "fields": (
                    "consent_reviewed",
                    "study_questions",
                    "assessment_score",
                    "consent_signature",
                    "consent_copy",
                ),
                "description": _("The following questions are directed to the interviewer."),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "subject_consent",
        "report_date",
        "agrees",
    )

    list_filter = (
        "report_datetime",
        AgreesListFilter,
    )

    radio_fields = {  # noqa: RUF012
        "agrees_to_extension": admin.VERTICAL,
        "consent_reviewed": admin.VERTICAL,
        "study_questions": admin.VERTICAL,
        "assessment_score": admin.VERTICAL,
        "consent_signature": admin.VERTICAL,
        "consent_copy": admin.VERTICAL,
    }

    def get_readonly_fields(self, request, obj=None) -> tuple[str, ...]:  # noqa: ARG002
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

    @admin.display(description="Agrees")
    def agrees(self, obj):
        return obj.agrees_to_extension

    @admin.display(description="Report date")
    def report_date(self, obj):
        if obj:
            return obj.report_datetime.date()
        return None
