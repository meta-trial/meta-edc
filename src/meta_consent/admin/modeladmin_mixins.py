from django.contrib import admin, messages
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django_audit_fields.admin import audit_fieldset_tuple
from edc_consent.actions import (
    flag_as_verified_against_paper,
    unflag_as_verified_against_paper,
)
from edc_identifier import SubjectIdentifierError, is_subject_identifier_or_raise
from edc_pharmacy.exceptions import PrescriptionAlreadyExists
from edc_pharmacy.models import Medication
from edc_pharmacy.prescribe import create_prescription

from meta_edc.meta_version import get_meta_version
from meta_pharmacy.constants import METFORMIN
from meta_screening.models.subject_screening import SubjectScreening
from meta_subject.models import SubjectVisit

from ..forms import SubjectConsentForm
from ..models import SubjectConsent


class SubjectConsentModelAdminMixin:
    form = SubjectConsentForm

    actions = (
        flag_as_verified_against_paper,
        unflag_as_verified_against_paper,
        "create_missing_metformin_rx",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "screening_identifier",
                    "subject_identifier",
                    "first_name",
                    "last_name",
                    "initials",
                    "gender",
                    "language",
                    "is_literate",
                    "witness_name",
                    "consent_datetime",
                    "dob",
                    "guardian_name",
                    "is_dob_estimated",
                    "identity",
                    "identity_type",
                    "confirm_identity",
                    "is_incarcerated",
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

    search_fields = ("subject_identifier", "screening_identifier", "identity")

    radio_fields = {  # noqa: RUF012
        "gender": admin.VERTICAL,
        "assessment_score": admin.VERTICAL,
        "consent_copy": admin.VERTICAL,
        "consent_reviewed": admin.VERTICAL,
        "consent_signature": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "is_incarcerated": admin.VERTICAL,
        "is_literate": admin.VERTICAL,
        "language": admin.VERTICAL,
        "study_questions": admin.VERTICAL,
    }

    def delete_view(self, request, object_id, extra_context=None):
        """Prevent deletion if SubjectVisit objects exist."""
        extra_context = extra_context or {}
        obj = SubjectConsent.objects.get(id=object_id)
        try:
            protected = [SubjectVisit.objects.get(subject_identifier=obj.subject_identifier)]
        except ObjectDoesNotExist:
            protected = None
        except MultipleObjectsReturned:
            protected = SubjectVisit.objects.filter(subject_identifier=obj.subject_identifier)
        extra_context.update({"protected": protected})
        return super().delete_view(request, object_id, extra_context)

    def get_next_options(self, request=None, **kwargs):
        """Returns the key/value pairs from the "next" querystring
        as a dictionary.
        """
        next_options = super().get_next_options(request=request, **kwargs)
        try:
            is_subject_identifier_or_raise(next_options["subject_identifier"])
        except SubjectIdentifierError:
            next_options["subject_identifier"] = SubjectScreening.objects.get(
                subject_identifier_as_pk=next_options["subject_identifier"]
            ).subject_identifier
        except KeyError:
            pass
        return next_options

    @admin.action(permissions=["view"], description=_("Create missing METFORMIN prescription"))
    def create_missing_metformin_rx(self, request, queryset):
        medication = Medication.objects.get(name=METFORMIN)
        total = queryset.count()
        created = 0
        exist = 0
        for instance in queryset:
            try:
                create_prescription(
                    subject_identifier=instance.subject_identifier,
                    report_datetime=instance.consent_datetime,
                    randomizer_name=get_meta_version(),
                    medication_names=[medication.name],
                    site_id=instance.site.id,
                )
            except PrescriptionAlreadyExists:
                exist += 1
            else:
                created += 1
        messages.success(
            request,
            _(
                "Created %(created)s/%(total)s missing %(display_name)s prescriptions. "
                "Got %(exist)s/%(total)s prescriptions already exist"
            )
            % {
                "created": created,
                "exist": exist,
                "total": total,
                "display_name": medication.display_name,
            },
        )
