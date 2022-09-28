import sys
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from edc_offstudy.exceptions import OffstudyError
from edc_pharmacy.exceptions import NextStudyMedicationError, StudyMedicationError
from edc_pharmacy.models import DosageGuideline, Formulation, Medication
from edc_pharmacy.refill.refill_creator import RefillCreatorError
from edc_visit_schedule.utils import is_baseline
from tqdm import tqdm

from meta_pharmacy.constants import METFORMIN
from meta_subject.models import StudyMedication


def create_missing_rx_refills():
    messages = []
    medication = Medication.objects.get(name=METFORMIN)
    formulation = Formulation.objects.get(medication=medication, strength=500)
    dosage_guideline_baseline = DosageGuideline.objects.get(
        medication=medication, dose=Decimal("1000.0")
    )
    dosage_guideline_followup = DosageGuideline.objects.get(
        medication=medication, dose=Decimal("2000.0")
    )
    qs = StudyMedication.objects.all()
    total = qs.count()
    for obj in tqdm(qs, total=total):
        obj.refill_identifier = obj.id
        if not obj.formulation:
            obj.formulation = formulation
        if not obj.dosage_guideline:
            if is_baseline(obj.related_visit):
                obj.dosage_guideline = dosage_guideline_baseline
            else:
                obj.dosage_guideline = dosage_guideline_followup
        messages = save_or_raise(obj, messages=messages)
    print_messages(messages)


def save_or_raise(obj, messages: list[str] = None):
    try:
        obj.save()
    except NextStudyMedicationError as e:
        messages.append(f"NextStudyMedicationError: {e}")
    except ObjectDoesNotExist as e:
        messages.append(
            f"ObjectDoesNotExist: {obj.subject_identifier}, {obj.related_visit}, {str(e)}"
        )
    except StudyMedicationError as e:
        messages.append(f"StudyMedicationError: {e}")
    except RefillCreatorError as e:
        messages.append(f"RefillCreatorError: {e}")
    except OffstudyError as e:
        messages.append(f"OffstudyError: {e}")
    return messages


def print_messages(messages: list[str]):
    sys.stdout.write("\n")
    for message in messages:
        sys.stdout.write("\n")
        sys.stdout.write(message)


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_missing_rx_refills()
