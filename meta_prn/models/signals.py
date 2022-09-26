from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_constants.constants import YES
from edc_visit_schedule import site_visit_schedules

from meta_subject.models import SubjectVisit, UrinePregnancy
from meta_visit_schedule.constants import SCHEDULE, SCHEDULE_PREGNANCY, VISIT_SCHEDULE

from .offschedule import OffSchedule
from .pregnancy_notification import PregnancyNotification


@receiver(
    post_save,
    weak=False,
    sender=PregnancyNotification,
    dispatch_uid="update_schedule_on_pregnancy_notification_post_save",
)
def update_schedule_on_pregnancy_notification_post_save(sender, instance, raw, **kwargs):

    if not raw:
        try:
            OffSchedule.objects.get(subject_identifier=instance.subject_identifier)
        except ObjectDoesNotExist:
            last_subject_visit = (
                SubjectVisit.objects.filter(
                    subject_identifier=instance.subject_identifier,
                    schedule_name=SCHEDULE,
                )
                .order_by("report_datetime")
                .last()
            )
            visit_schedule = site_visit_schedules.get_visit_schedule(
                visit_schedule_name=VISIT_SCHEDULE
            )
            schedule = visit_schedule.schedules.get(SCHEDULE)
            schedule.take_off_schedule(
                offschedule_datetime=last_subject_visit.report_datetime,
                subject_identifier=instance.subject_identifier,
            )
            schedule = visit_schedule.schedules.get(SCHEDULE_PREGNANCY)
            schedule.put_on_schedule(
                onschedule_datetime=last_subject_visit.report_datetime,
                subject_identifier=instance.subject_identifier,
            )


@receiver(
    post_save,
    weak=False,
    sender=PregnancyNotification,
    dispatch_uid="update_urine_pregnancy_on_pregnancy_notification_on_post_save",
)
def update_urine_pregnancy_on_pregnancy_notification_on_post_save(
    sender, instance, raw, **kwargs
):
    if not raw:
        if instance.bhcg_confirmed == YES:
            UrinePregnancy.objects.filter(
                subject_visit__subject_identifier=instance.subject_identifier,
                notified=False,
                assay_date__lte=instance.report_datetime.date(),
            ).update(
                notified_datetime=instance.report_datetime,
                notified=True,
            )
