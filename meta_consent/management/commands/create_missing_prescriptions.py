from django.core.management.base import BaseCommand, CommandError
from edc_pharmacy.models import Medication, Rx
from edc_pharmacy.utils import create_prescription

from meta_consent.models import SubjectConsent
from meta_edc.meta_version import get_meta_version


class Command(BaseCommand):
    help = "Create missing prescriptions"

    def handle(self, *args, **options):
        medication = Medication.objects.get(name="metformin")
        subject_identifiers = Rx.objects.values_list(
            "subject_identifier", flat=True
        ).all()
        for instance in SubjectConsent.objects.exclude(
            subject_identifier__in=subject_identifiers
        ):
            create_prescription(
                subject_identifier=instance.subject_identifier,
                report_datetime=instance.consent_datetime,
                randomizer_name=get_meta_version(),
                medication_name=medication.name,
            )
