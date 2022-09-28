from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from edc_constants.constants import YES
from edc_pharmacy.exceptions import PrescriptionAlreadyExists, StudyMedicationError
from edc_pharmacy.models import DosageGuideline, Formulation, Medication, RxRefill
from edc_pharmacy.prescribe import create_prescription
from edc_registration.models import RegisteredSubject

from meta_pharmacy.constants import METFORMIN
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.models import StudyMedication


class TestStudyMedication(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()
        self.registered_subject = RegisteredSubject.objects.get(
            subject_identifier=self.subject_visit.subject_identifier
        )

    def test_rx_exists(self):
        medication = Medication.objects.get(name=METFORMIN)
        self.assertRaises(
            PrescriptionAlreadyExists,
            create_prescription,
            subject_identifier=self.registered_subject.subject_identifier,
            report_datetime=self.registered_subject.registration_datetime,
            medications=[medication],
            site=self.registered_subject.site,
        )

    def test_missing_formulation(self):
        obj = StudyMedication(subject_visit=self.subject_visit)
        with self.assertRaises(StudyMedicationError) as cm:
            obj.save()
        self.assertIn("Formulation", str(cm.exception))

    def test_missing_dosage_guideline(self):
        medication = Medication.objects.get(name=METFORMIN)
        formulation = Formulation.objects.filter(medication=medication)[0]
        obj = StudyMedication(
            subject_visit=self.subject_visit,
            refill_start_datetime=self.subject_visit.report_datetime,
            refill_to_next_visit=YES,
            formulation=formulation,
        )
        with self.assertRaises(StudyMedicationError) as cm:
            obj.save()
        self.assertIn("Dosage guideline", str(cm.exception))

    def test_study_med_longitudinal_and_one_rx_refill_created(self):
        medication = Medication.objects.get(name=METFORMIN)
        formulation = Formulation.objects.filter(medication=medication)[0]
        dosage_guideline = DosageGuideline.objects.filter(medication=medication)[0]
        obj = StudyMedication(
            subject_visit=self.subject_visit,
            refill_start_datetime=self.subject_visit.report_datetime,
            formulation=formulation,
            dosage_guideline=dosage_guideline,
            refill_to_next_visit=YES,
        )
        obj.save()
        try:
            RxRefill.objects.get(
                rx=obj.rx,
                rx__subject_identifier=self.subject_visit.subject_identifier,
                refill_start_datetime=obj.refill_start_datetime,
            )
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised")

        self.assertEqual(RxRefill.objects.filter(rx=obj.rx).count(), 1)

    def test_study_med_longitudinal_updated_and_same_rx_refill_updated(self):
        """Assert study med update operates on same rx_refill when updated"""
        medication = Medication.objects.get(name=METFORMIN)
        formulation = Formulation.objects.filter(medication=medication)[0]
        dosage_guideline = DosageGuideline.objects.filter(medication=medication)[0]
        obj = StudyMedication(
            subject_visit=self.subject_visit,
            refill_start_datetime=self.subject_visit.report_datetime,
            formulation=formulation,
            dosage_guideline=dosage_guideline,
            refill_to_next_visit=YES,
        )
        obj.save()
        obj.save()
        self.assertEqual(RxRefill.objects.filter(rx=obj.rx).count(), 1)
        changed_dosage_guideline = DosageGuideline.objects.filter(medication=medication)[1]
        obj.dosage_guideline = changed_dosage_guideline
        obj.save()
        self.assertEqual(RxRefill.objects.filter(rx=obj.rx).count(), 1)
        rx = RxRefill.objects.get(rx=obj.rx)
        self.assertEqual(rx.dosage_guideline, obj.dosage_guideline)

    def test_study_med_longitudinal_update_start_datetime_and_same_rx_refill_updated(self):
        """Assert study med update operates on same rx_refill when updated"""
        medication = Medication.objects.get(name=METFORMIN)
        formulation = Formulation.objects.filter(medication=medication)[0]
        dosage_guideline = DosageGuideline.objects.filter(medication=medication)[0]
        obj = StudyMedication(
            subject_visit=self.subject_visit,
            refill_start_datetime=self.subject_visit.report_datetime,
            formulation=formulation,
            dosage_guideline=dosage_guideline,
            refill_to_next_visit=YES,
        )
        obj.save()
        obj.save()
        self.assertEqual(RxRefill.objects.filter(rx=obj.rx).count(), 1)
        obj.refill_start_datetime = obj.refill_start_datetime + relativedelta(hours=1)
        obj.save()
        self.assertEqual(RxRefill.objects.filter(rx=obj.rx).count(), 1)
        rx = RxRefill.objects.get(rx=obj.rx)
        self.assertEqual(rx.refill_start_datetime, obj.refill_start_datetime)

    def test_study_med_longitudinal_and_one_rx_refill_created2(self):
        medication = Medication.objects.get(name=METFORMIN)
        formulation = Formulation.objects.filter(medication=medication)[0]
        dosage_guideline = DosageGuideline.objects.filter(medication=medication)[0]
        obj = StudyMedication(
            subject_visit=self.subject_visit,
            refill_start_datetime=self.subject_visit.report_datetime,
            formulation=formulation,
            dosage_guideline=dosage_guideline,
            refill_to_next_visit=YES,
        )
        obj.save()
        try:
            RxRefill.objects.get(
                rx=obj.rx,
                rx__subject_identifier=self.subject_visit.subject_identifier,
                refill_start_datetime=obj.refill_start_datetime,
            )
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised")

        self.assertEqual(RxRefill.objects.filter(rx=obj.rx).count(), 1)

        try:
            RxRefill.objects.get(refill_identifier=obj.refill_identifier)
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised")

    def test_study_med_longitudinal_and_two_rx_refill_created(self):
        date_sequence = []
        medication = Medication.objects.get(name=METFORMIN)
        formulation = Formulation.objects.filter(medication=medication)[0]
        dosage_guideline = DosageGuideline.objects.filter(medication=medication)[0]
        subject_visits = [self.subject_visit, self.get_next_subject_visit(self.subject_visit)]
        for i in [1, 2]:
            subject_visit = subject_visits[i - 1]
            obj = StudyMedication(
                subject_visit=subject_visit,
                refill_start_datetime=subject_visit.report_datetime,
                formulation=formulation,
                dosage_guideline=dosage_guideline,
                refill_to_next_visit=YES,
            )
            obj.save()
            date_sequence.append(obj.refill_start_datetime)
            try:
                RxRefill.objects.get(
                    rx=obj.rx,
                    rx__subject_identifier=subject_visit.subject_identifier,
                    refill_start_datetime=obj.refill_start_datetime,
                )
            except ObjectDoesNotExist:
                self.fail("ObjectDoesNotExist unexpectedly raised")

            self.assertEqual(RxRefill.objects.filter(rx=obj.rx).count(), i)

            try:
                rx_refill = RxRefill.objects.get(refill_identifier=obj.refill_identifier)
            except ObjectDoesNotExist:
                self.fail("ObjectDoesNotExist unexpectedly raised")
            date_sequence.append(rx_refill.refill_end_datetime)
        dte1, dte2, dte3, dte4 = date_sequence
        self.assertTrue(dte1 <= dte2 <= dte3 <= dte4)

    def test_study_med_longitudinal(self):
        StudyMedication(
            subject_visit=self.subject_visit,
            refill_start_datetime=self.subject_visit.report_datetime,
            refill_to_next_visit=YES,
        )
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        StudyMedication(
            subject_visit=subject_visit,
            refill_start_datetime=subject_visit.report_datetime,
            refill_to_next_visit=YES,
        )
        subject_visit = self.get_next_subject_visit(subject_visit)
        StudyMedication(
            subject_visit=subject_visit,
            refill_start_datetime=subject_visit.report_datetime,
            refill_to_next_visit=YES,
        )
        subject_visit = self.get_next_subject_visit(subject_visit)
        StudyMedication(
            subject_visit=subject_visit,
            refill_start_datetime=subject_visit.report_datetime,
            refill_to_next_visit=YES,
        )
        subject_visit = self.get_next_subject_visit(subject_visit)
        StudyMedication(
            subject_visit=subject_visit,
            refill_start_datetime=subject_visit.report_datetime,
            refill_to_next_visit=YES,
        )
        subject_visit = self.get_next_subject_visit(subject_visit)
        StudyMedication(
            subject_visit=subject_visit,
            refill_start_datetime=subject_visit.report_datetime,
            refill_to_next_visit=YES,
        )
        subject_visit = self.get_next_subject_visit(subject_visit)
        StudyMedication(
            subject_visit=subject_visit,
            refill_start_datetime=subject_visit.report_datetime,
            refill_to_next_visit=YES,
        )
        subject_visit = self.get_next_subject_visit(subject_visit)
        StudyMedication(
            subject_visit=subject_visit,
            refill_start_datetime=subject_visit.report_datetime,
            refill_to_next_visit=YES,
        )
