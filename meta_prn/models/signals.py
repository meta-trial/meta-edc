from django.db.models.signals import post_save
from django.dispatch import receiver

from meta_prn.models import PregnancyNotification
from meta_subject.models import UrinePregnancy


@receiver(
    post_save,
    weak=False,
    sender=PregnancyNotification,
    dispatch_uid="update_urine_pregnancy_on_notification_on_post_save",
)
def update_urine_pregnancy_on_notification_on_post_save(
    sender, instance, raw, **kwargs
):
    if not raw:
        UrinePregnancy.objects.filter(
            subject_visit__subject_identifier=instance.subject_identifier,
            notified=False,
            assay_date__lte=instance.report_datetime.date(),
        ).update(
            notified_datetime=instance.report_datetime,
            notified=True,
        )
