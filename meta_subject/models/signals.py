from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from edc_appointment.models import Appointment
from edc_consent.utils import get_consent_model_cls
from edc_pharmacy.exceptions import PrescriptionAlreadyExists
from edc_pharmacy.prescribe import create_prescription
from edc_visit_schedule import site_visit_schedules
from edc_visit_schedule.constants import DAY1

from meta_edc.meta_version import get_meta_version
from meta_pharmacy.constants import METFORMIN
from meta_visit_schedule.constants import (
    SCHEDULE_POSTNATAL,
    SCHEDULE_PREGNANCY,
    VISIT_SCHEDULE,
)

from .delivery import Delivery
from .study_medication import StudyMedication
from .subject_visit import SubjectVisit


@receiver(
    pre_save,
    weak=False,
    sender=StudyMedication,
    dispatch_uid="study_medication_on_pre_save",
)
def study_medication_on_pre_save(sender, instance, raw, **kwargs):
    """Create a prescription if one does not exist

    All refills are created against the prescription

    Note: this should not be necessary if consented after meta_consent.signal
          was updated to call `create_prescription`.
    """
    if not raw and instance.subject_visit.visit_code == DAY1:
        subject_consent = get_consent_model_cls().objects.get(
            subject_identifier=instance.subject_visit.subject_identifier,
        )
        try:
            create_prescription(
                subject_identifier=subject_consent.subject_identifier,
                report_datetime=subject_consent.consent_datetime,
                randomizer_name=get_meta_version(),
                medications=[METFORMIN],
                site=subject_consent.site,
            )
        except PrescriptionAlreadyExists:
            pass


@receiver(
    post_save,
    weak=False,
    sender=Delivery,
    dispatch_uid="update_pregnancy_notification_on_delivery_post_save",
)
def update_pregnancy_notification_on_delivery_post_save(sender, instance, raw, **kwargs):
    """Updates PregnancyNotification model instance when the delivery form is submitted.

    Sets delivered=True and delivery_datetime
    """
    if not raw:
        model_cls = django_apps.get_model("meta_prn.pregnancynotification")
        model_cls.objects.filter(
            subject_identifier=instance.subject_visit.subject_identifier,
            delivered=False,
            delivery_datetime=None,
        ).update(delivered=True, delivery_datetime=instance.delivery_datetime)


@receiver(
    post_save,
    weak=False,
    sender=Delivery,
    dispatch_uid="update_schedule_on_delivery_post_save",
)
def update_schedule_on_delivery_post_save(sender, instance, raw, **kwargs):
    """Takes a participant off the SCHEDULE_PREGNANCY schedule and puts them on
    SCHEDULE_POSTNATAL when delivery form is submitted.

    - gets last report_datetime of the subject visit for SCHEDULE_PREGNANCY
    - take_off_schedule SCHEDULE_PREGNANCY using the last visit datetime
    - put_on_schedule SCHEDULE_POSTNATAL
    - sets first appointment of SCHEDULE_POSTNATAL to be 36 months from baseline
    """
    if not raw:
        offschedule_model_cls = django_apps.get_model("meta_prn.offschedulepregnancy")
        try:
            offschedule_model_cls.objects.get(subject_identifier=instance.subject_identifier)
        except ObjectDoesNotExist:
            last_subject_visit = (
                SubjectVisit.objects.filter(
                    subject_identifier=instance.subject_identifier,
                    schedule_name=SCHEDULE_PREGNANCY,
                )
                .order_by("report_datetime")
                .last()
            )
            visit_schedule = site_visit_schedules.get_visit_schedule(
                visit_schedule_name=VISIT_SCHEDULE
            )
            schedule = visit_schedule.schedules.get(SCHEDULE_PREGNANCY)
            schedule.take_off_schedule(
                offschedule_datetime=last_subject_visit.report_datetime,
                subject_identifier=instance.subject_identifier,
            )
            schedule = visit_schedule.schedules.get(SCHEDULE_POSTNATAL)

            first_appt_datetime = Appointment.objects.get(
                subject_identifier=instance.subject_identifier,
                visit_code=DAY1,
                visit_code_sequence=0,
                timepoint=0,
            ).appt_datetime + relativedelta(months=36)

            schedule.put_on_schedule(
                onschedule_datetime=last_subject_visit.report_datetime,
                subject_identifier=instance.subject_identifier,
                first_appt_datetime=first_appt_datetime,
            )
