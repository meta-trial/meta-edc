import sys

from django.core.management import BaseCommand
from edc_consent.utils import get_consent_model_cls
from edc_pharmacy.exceptions import PrescriptionAlreadyExists
from edc_pharmacy.prescribe import create_prescription
from edc_visit_schedule.constants import DAY1
from tqdm import tqdm

from meta_edc.meta_version import get_meta_version
from meta_pharmacy.constants import METFORMIN
from meta_subject.models import SubjectVisit


def create_missing_rx():
    n = 0
    sys.stdout.write("\nCreate missing prescriptions...\n")
    cnt = SubjectVisit.objects.filter(visit_code=DAY1, visit_code_sequence=0).count()
    for subject_visit in tqdm(
        SubjectVisit.objects.filter(visit_code=DAY1, visit_code_sequence=0), total=cnt
    ):
        subject_consent = get_consent_model_cls().objects.get(
            subject_identifier=subject_visit.subject_identifier,
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
        else:
            n += 1

    sys.stdout.write(f"\nCreated {n}/{cnt}. Done.\n")


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_missing_rx()
