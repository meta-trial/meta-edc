import contextlib

from clinicedc_constants import YES
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from edc_action_item.delete_action_item import ActionItemDeleteError, delete_action_item
from edc_pharmacy.exceptions import PrescriptionAlreadyExists
from edc_pharmacy.prescribe import create_prescription
from edc_randomization.site_randomizers import site_randomizers
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from meta_edc.meta_version import get_meta_version
from meta_screening.models import SubjectScreening
from meta_subject.models import SubjectVisit

from ..action_items import ReconsentAction
from .subject_consent import SubjectConsent
from .subject_consent_v1 import SubjectConsentV1


@receiver(
    post_save,
    weak=False,
    sender=SubjectConsentV1,
    dispatch_uid="subject_consent_on_post_save",
)
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):  # noqa: ARG001
    """Creates an onschedule instance for this consented subject, if
    it does not exist.
    """

    if not raw:
        if not created:
            _, schedule = site_visit_schedules.get_by_onschedule_model("meta_prn.onschedule")
            schedule.refresh_schedule(instance.subject_identifier)
        else:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=instance.screening_identifier
            )
            if not subject_screening.consented:
                subject_screening.subject_identifier = instance.subject_identifier
                subject_screening.consented = True
                subject_screening.save_base(update_fields=["subject_identifier", "consented"])

                # randomize
                site_randomizers.randomize(
                    get_meta_version(),
                    identifier=instance.subject_identifier,
                    report_datetime=instance.consent_datetime,
                    site=instance.site,
                    user=instance.user_created,
                    gender=instance.gender,
                )

                # put subject on schedule
                _, schedule = site_visit_schedules.get_by_onschedule_model(
                    "meta_prn.onschedule"
                )
                schedule.put_on_schedule(
                    subject_identifier=instance.subject_identifier,
                    onschedule_datetime=instance.consent_datetime,
                )
                # All refills are created against this prescription
                with contextlib.suppress(PrescriptionAlreadyExists):
                    create_prescription(
                        subject_identifier=instance.subject_identifier,
                        report_datetime=instance.consent_datetime,
                        medication_names=[instance.study_medication_name],
                        randomizer_name=get_meta_version(),
                        site=instance.site,
                    )

        # create / delete action for reconsent
        if instance.completed_by_next_of_kin == YES:
            ReconsentAction(subject_identifier=instance.subject_identifier)
        else:
            with contextlib.suppress(ActionItemDeleteError):
                delete_action_item(
                    action_cls=ReconsentAction,
                    subject_identifier=instance.subject_identifier,
                )


# @receiver(
#     post_save,
#     weak=False,
#     sender=SubjectConsentV1Ext,
#     dispatch_uid="subject_consent_v1_ext_on_post_save",
# )
# def subject_consent_v1_ext_on_post_save(sender, instance, raw, created, **kwargs):
#     if not raw:
#         refresh_appointments(
#             subject_identifier=instance.subject_identifier,
#             visit_schedule_name=VISIT_SCHEDULE,
#             schedule_name=SCHEDULE,
#         )


@receiver(
    post_delete,
    weak=False,
    dispatch_uid="subject_consent_on_post_delete",
)
def subject_consent_on_post_delete(sender, instance, using, **kwargs):  # noqa: ARG001
    """Updates/Resets subject screening."""
    # don't allow if subject visits exist. This should be caught
    # in the ModelAdmin delete view
    if sender in [SubjectConsent, SubjectConsentV1]:
        if SubjectVisit.objects.filter(
            subject_identifier=instance.subject_identifier
        ).exists():
            raise ValidationError("Unable to delete consent. Visit data exists.")

        _, schedule = site_visit_schedules.get_by_onschedule_model("meta_prn.onschedule")
        schedule.take_off_schedule(instance.subject_identifier, instance.consent_datetime)

        # update subject screening
        subject_screening = SubjectScreening.objects.get(
            screening_identifier=instance.screening_identifier
        )
        subject_screening.consented = False
        subject_screening.subject_identifier = subject_screening.subject_screening_as_pk
        subject_screening.save()
