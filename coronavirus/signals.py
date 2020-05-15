from django.apps import apps as django_apps
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_registration.models import RegisteredSubject

from .models import CoronaKap


@receiver(
    post_save,
    weak=False,
    dispatch_uid="update_kap_identifiers_post_save",
    sender=CoronaKap,
)
def update_kap_identifiers_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw and not kwargs.get("update_fields"):
        if instance.subject_identifier and not instance.screening_identifier:
            registered_subject = RegisteredSubject.objects.get(
                subject_identifier=instance.subject_identifier
            )
            instance.screening_identifier = registered_subject.screening_identifier
            instance.save_base(update_fields=["screening_identifier"])
        elif not instance.subject_identifier and instance.screening_identifier:
            model_cls = django_apps.get_model(settings.SUBJECT_SCREENING_MODEL)
            subject_screening = model_cls.objects.get(
                screening_identifier=instance.screening_identifier
            )
            instance.subject_identifier = subject_screening.subject_identifier
            instance.save_base(update_fields=["subject_identifier"])
