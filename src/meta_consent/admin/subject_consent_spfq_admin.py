from django.contrib import admin
from django.utils.translation import gettext as _
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_consent_admin
from ..forms import SubjectConsentSpfqForm
from ..models import SubjectConsentSpfq


@admin.register(SubjectConsentSpfq, site=meta_consent_admin)
class SubjectConsentSpfqAdmin(
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentSpfqForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "initials",
                    "gender",
                    "language",
                    "consent_datetime",
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

    search_fields = ("subject_identifier",)

    radio_fields = {  # noqa: RUF012
        "gender": admin.VERTICAL,
        "assessment_score": admin.VERTICAL,
        "consent_copy": admin.VERTICAL,
        "consent_reviewed": admin.VERTICAL,
        "consent_signature": admin.VERTICAL,
        "language": admin.VERTICAL,
        "study_questions": admin.VERTICAL,
    }
