from datetime import datetime
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, override_settings
from edc_constants.constants import NO, YES
from edc_utils import get_utcnow
from model_bakery import baker

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.models import SubjectVisit
from meta_visit_schedule.constants import (
    MONTH1,
    MONTH3,
    MONTH6,
    MONTH9,
    MONTH12,
    MONTH15,
    MONTH18,
    MONTH21,
    MONTH24,
    MONTH27,
    MONTH30,
    MONTH33,
    MONTH36,
    MONTH39,
    MONTH42,
    MONTH45,
    MONTH48,
    WEEK2,
)

test_datetime = datetime(2019, 6, 11, 8, 00, tzinfo=ZoneInfo("UTC"))


@override_settings(
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=test_datetime - relativedelta(years=3),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=test_datetime + relativedelta(years=3),
)
class TestMnsiRequired(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        traveller = time_machine.travel(test_datetime)
        traveller.start()
        self.baseline_datetime = get_utcnow()

        self.subject_screening = self.get_subject_screening(
            report_datetime=self.baseline_datetime,
            eligibility_datetime=self.baseline_datetime,
        )
        self.subject_consent = self.get_subject_consent(
            self.subject_screening,
            consent_datetime=self.baseline_datetime,
        )

        self.subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            appt_datetime=self.baseline_datetime,
        )
        traveller.stop()

    def get_visit(self, visit_code: str):
        """Returns a scheduled visit with the specified visit code.

        If the visit already exists, it will be returned. If not, it
        will be created (along with any interim visits) and returned.
        """
        subject_identifier = self.subject_consent.subject_identifier
        try:
            subject_visit = SubjectVisit.objects.get(
                subject_identifier=subject_identifier,
                visit_code=visit_code,
                visit_code_sequence=0,
            )
        except ObjectDoesNotExist:
            subject_visit = (
                SubjectVisit.objects.filter(
                    subject_identifier=subject_identifier,
                    visit_code_sequence=0,
                )
                .order_by("visit_code")
                .last()
            )
            while subject_visit.visit_code != visit_code:
                subject_visit = self.get_next_subject_visit(subject_visit)

        self.assertEqual(subject_visit.visit_code, visit_code)
        self.assertEqual(subject_visit.visit_code_sequence, 0)
        return subject_visit

    @staticmethod
    def set_mnsi_status(subject_visit, mnsi_performed):
        visit_mnsi = baker.make(
            "meta_subject.mnsi",
            report_datetime=subject_visit.report_datetime,
            subject_visit=subject_visit,
            mnsi_performed=mnsi_performed,
        )
        visit_mnsi.save()

    def test_mnsi_not_required_at_baseline(self):
        crfs = self.get_crf_metadata(self.subject_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_2w(self):
        crfs = self.get_crf_metadata(self.get_visit(visit_code=WEEK2))
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_required_at_1m(self):
        crfs = self.get_crf_metadata(self.get_visit(visit_code=MONTH1))
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_3m_if_already_performed_at_1m(self):
        # MNSI shouldn't be required at any point after it has been performed
        month1_visit = self.get_visit(visit_code=MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        month3_visit = self.get_visit(visit_code=MONTH3)
        crfs = self.get_crf_metadata(month3_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_required_at_3m_if_not_performed_at_1m(self):
        month1_visit = self.get_visit(visit_code=MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        month3_visit = self.get_visit(visit_code=MONTH3)
        crfs = self.get_crf_metadata(month3_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_6m_if_already_performed_at_1m(self):
        # MNSI shouldn't be required at any point after it has been performed
        month1_visit = self.get_visit(visit_code=MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        month3_visit = self.get_visit(visit_code=MONTH3)
        crfs = self.get_crf_metadata(month3_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month6_visit = self.get_visit(visit_code=MONTH6)
        crfs = self.get_crf_metadata(month6_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_6m_if_already_performed_at_3m(self):
        month1_visit = self.get_visit(visit_code=MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        # MNSI shouldn't be required at any point after it has been performed
        month3_visit = self.get_visit(visit_code=MONTH3)
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=YES)

        month6_visit = self.get_visit(visit_code=MONTH6)
        crfs = self.get_crf_metadata(month6_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_required_at_6m_if_not_performed_by_3m(self):
        month1_visit = self.get_visit(visit_code=MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        month3_visit = self.get_visit(visit_code=MONTH3)
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=NO)

        month6_visit = self.get_visit(visit_code=MONTH6)
        crfs = self.get_crf_metadata(month6_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_9m_if_already_performed_at_1m(self):
        # MNSI shouldn't be required at any point after it has been performed
        month1_visit = self.get_visit(visit_code=MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        month3_visit = self.get_visit(visit_code=MONTH3)
        crfs = self.get_crf_metadata(month3_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month6_visit = self.get_visit(visit_code=MONTH6)
        crfs = self.get_crf_metadata(month6_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month9_visit = self.get_visit(visit_code=MONTH9)
        crfs = self.get_crf_metadata(month9_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_9m_if_already_performed_at_3m(self):
        month1_visit = self.get_visit(visit_code=MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        # MNSI shouldn't be required at any point after it has been performed
        month3_visit = self.get_visit(visit_code=MONTH3)
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=YES)

        month6_visit = self.get_visit(visit_code=MONTH6)
        crfs = self.get_crf_metadata(month6_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month9_visit = self.get_visit(visit_code=MONTH9)
        crfs = self.get_crf_metadata(month9_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_9m_if_already_performed_at_6m(self):
        month1_visit = self.get_visit(visit_code=MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        month3_visit = self.get_visit(visit_code=MONTH3)
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=NO)

        # MNSI shouldn't be required at any point after it has been performed
        month6_visit = self.get_visit(visit_code=MONTH6)
        self.set_mnsi_status(subject_visit=month6_visit, mnsi_performed=YES)

        month9_visit = self.get_visit(visit_code=MONTH9)
        crfs = self.get_crf_metadata(month9_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_between_9m_and_33m_when_performed_in_first_6m(self):
        month1_visit = self.get_visit(visit_code=MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        month3_visit = self.get_visit(visit_code=MONTH3)
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=YES)

        for visit_code in [
            MONTH9,
            MONTH12,
            MONTH15,
            MONTH18,
            MONTH21,
            MONTH24,
            MONTH27,
            MONTH30,
            MONTH33,
        ]:
            with self.subTest(visit_code=visit_code):
                subject_visit = self.get_visit(visit_code=visit_code)
                self.assertEqual(subject_visit.visit_code, visit_code)
                self.assertEqual(subject_visit.visit_code_sequence, 0)
                crfs = self.get_crf_metadata(subject_visit)
                self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_between_9m_and_33m_even_if_not_performed_first_6m(self):
        month1_visit = self.get_visit(visit_code=MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        month3_visit = self.get_visit(visit_code=MONTH3)
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=NO)

        month6_visit = self.get_visit(visit_code=MONTH6)
        self.set_mnsi_status(subject_visit=month6_visit, mnsi_performed=NO)

        for visit_code in [
            MONTH9,
            MONTH12,
            MONTH15,
            MONTH18,
            MONTH21,
            MONTH24,
            MONTH27,
            MONTH30,
            MONTH33,
        ]:
            with self.subTest(visit_code=visit_code):
                subject_visit = self.get_visit(visit_code=visit_code)
                self.assertEqual(subject_visit.visit_code, visit_code)
                self.assertEqual(subject_visit.visit_code_sequence, 0)
                crfs = self.get_crf_metadata(subject_visit)
                self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_required_between_36m_and_45m(self):
        traveller = time_machine.travel(datetime(2024, 12, 17, tzinfo=ZoneInfo("UTC")))
        traveller.start()
        self.get_subject_consent_extended(self.subject_consent, consent_datetime=get_utcnow())
        traveller.stop()

        month1_visit = self.get_visit(visit_code=MONTH1)
        traveller = time_machine.travel(month1_visit.report_datetime)
        traveller.start()
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        for visit_code in [MONTH36, MONTH39, MONTH42, MONTH45]:
            with self.subTest(visit_code=visit_code):
                subject_visit = self.get_visit(visit_code=visit_code)
                crfs = self.get_crf_metadata(subject_visit)
                self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
                self.set_mnsi_status(subject_visit=subject_visit, mnsi_performed=NO)
        traveller.stop()

    def test_mnsi_only_required_once_between_36m_and_45m(self):
        traveller = time_machine.travel(datetime(2024, 12, 17, tzinfo=ZoneInfo("UTC")))
        traveller.start()
        self.get_subject_consent_extended(self.subject_consent, consent_datetime=get_utcnow())
        month1_visit = self.get_visit(visit_code=MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        month36_visit = self.get_visit(visit_code=MONTH36)
        crfs = self.get_crf_metadata(month36_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.set_mnsi_status(subject_visit=month36_visit, mnsi_performed=NO)

        month39_visit = self.get_next_subject_visit(month36_visit)
        crfs = self.get_crf_metadata(month39_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.set_mnsi_status(subject_visit=month39_visit, mnsi_performed=NO)

        month42_visit = self.get_next_subject_visit(month39_visit)
        crfs = self.get_crf_metadata(month42_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.set_mnsi_status(subject_visit=month42_visit, mnsi_performed=YES)

        month45_visit = self.get_next_subject_visit(month42_visit)
        crfs = self.get_crf_metadata(month45_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        traveller.stop()

    def test_mnsi_required_at_48m(self):
        traveller = time_machine.travel(datetime(2024, 12, 16, tzinfo=ZoneInfo("UTC")))
        traveller.start()
        self.get_subject_consent_extended(self.subject_consent, consent_datetime=get_utcnow())
        month1_visit = self.get_visit(visit_code=MONTH1)
        crfs = self.get_crf_metadata(month1_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        month3_visit = self.get_next_subject_visit(month1_visit)
        crfs = self.get_crf_metadata(month3_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month36_visit = self.get_visit(visit_code=MONTH36)
        crfs = self.get_crf_metadata(month36_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.set_mnsi_status(subject_visit=month36_visit, mnsi_performed=YES)

        month39_visit = self.get_next_subject_visit(month36_visit)
        crfs = self.get_crf_metadata(month39_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month48_visit = self.get_visit(visit_code=MONTH48)
        crfs = self.get_crf_metadata(month48_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        traveller.stop()
