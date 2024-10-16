from datetime import datetime
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_constants.constants import NO, YES
from edc_utils import get_utcnow
from model_bakery import baker

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
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
    MONTH36,
    MONTH48,
    WEEK2,
)


@tag("mnsi")
@time_machine.travel(datetime(2022, 6, 11, 8, 00, tzinfo=ZoneInfo("UTC")))
class TestMnsiRequired(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.baseline_datetime = get_utcnow() - relativedelta(months=6)

        six_months_ago = self.baseline_datetime
        self.subject_screening = self.get_subject_screening(
            report_datetime=six_months_ago,
            eligibility_datetime=six_months_ago,
        )
        self.subject_consent = self.get_subject_consent(
            self.subject_screening,
            consent_datetime=six_months_ago,
        )
        self.subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            appt_datetime=six_months_ago,
        )

    def get_visit(self, visit_code: str, latest_visit):
        subject_visit = latest_visit
        while subject_visit.visit_code != visit_code:
            subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, visit_code)
        self.assertEqual(subject_visit.visit_code_sequence, 0)
        return subject_visit

    def get_week2_visit(self):
        return self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=WEEK2,
            appt_datetime=self.baseline_datetime + relativedelta(weeks=2),
        )

    def get_month1_visit(self):
        return self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=MONTH1,
            appt_datetime=self.baseline_datetime + relativedelta(months=1),
        )

    def get_month3_visit(self):
        return self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=MONTH3,
            appt_datetime=self.baseline_datetime + relativedelta(months=3),
        )

    def get_month6_visit(self):
        return self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=MONTH6,
            appt_datetime=self.baseline_datetime + relativedelta(months=6),
        )

    def get_month9_visit(self):
        return self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=MONTH9,
            appt_datetime=self.baseline_datetime + relativedelta(months=9),
        )

    @staticmethod
    def set_mnsi_status(subject_visit, mnsi_performed):
        visit_mnsi = baker.make(
            "meta_subject.mnsi",
            subject_visit=subject_visit,
            mnsi_performed=mnsi_performed,
        )
        visit_mnsi.save()

    def test_mnsi_not_required_at_baseline(self):
        crfs = self.get_crf_metadata(self.subject_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_2w(self):
        crfs = self.get_crf_metadata(self.get_week2_visit())
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_required_at_1m(self):
        self.get_week2_visit()

        month1_visit = self.get_month1_visit()
        crfs = self.get_crf_metadata(month1_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_3m_if_already_performed_at_1m(self):
        self.get_week2_visit()

        # MNSI shouldn't be required at any point after it has been performed
        month1_visit = self.get_month1_visit()
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        month3_visit = self.get_month3_visit()
        crfs = self.get_crf_metadata(month3_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_required_at_3m_if_not_performed_at_1m(self):
        self.get_week2_visit()

        month1_visit = self.get_month1_visit()
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        month3_visit = self.get_month3_visit()
        crfs = self.get_crf_metadata(month3_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_6m_if_already_performed_at_1m(self):
        self.get_week2_visit()

        # MNSI shouldn't be required at any point after it has been performed
        month1_visit = self.get_month1_visit()
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        month3_visit = self.get_month3_visit()
        crfs = self.get_crf_metadata(month3_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month6_visit = self.get_month6_visit()
        crfs = self.get_crf_metadata(month6_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_6m_if_already_performed_at_3m(self):
        self.get_week2_visit()

        month1_visit = self.get_month1_visit()
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        # MNSI shouldn't be required at any point after it has been performed
        month3_visit = self.get_month3_visit()
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=YES)

        month6_visit = self.get_month6_visit()
        crfs = self.get_crf_metadata(month6_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_required_at_6m_if_not_performed_by_3m(self):
        self.get_week2_visit()

        month1_visit = self.get_month1_visit()
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        month3_visit = self.get_month3_visit()
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=NO)

        month6_visit = self.get_month6_visit()
        crfs = self.get_crf_metadata(month6_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_9m_if_already_performed_at_1m(self):
        self.get_week2_visit()

        # MNSI shouldn't be required at any point after it has been performed
        month1_visit = self.get_month1_visit()
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        month3_visit = self.get_month3_visit()
        crfs = self.get_crf_metadata(month3_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month6_visit = self.get_month6_visit()
        crfs = self.get_crf_metadata(month6_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month9_visit = self.get_month9_visit()
        crfs = self.get_crf_metadata(month9_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_9m_if_already_performed_at_3m(self):
        self.get_week2_visit()

        month1_visit = self.get_month1_visit()
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        # MNSI shouldn't be required at any point after it has been performed
        month3_visit = self.get_month3_visit()
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=YES)

        month6_visit = self.get_month6_visit()
        crfs = self.get_crf_metadata(month6_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month9_visit = self.get_month9_visit()
        crfs = self.get_crf_metadata(month9_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_9m_if_already_performed_at_6m(self):
        self.get_week2_visit()

        month1_visit = self.get_month1_visit()
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        month3_visit = self.get_month3_visit()
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=NO)

        # MNSI shouldn't be required at any point after it has been performed
        month6_visit = self.get_month6_visit()
        self.set_mnsi_status(subject_visit=month6_visit, mnsi_performed=YES)

        month9_visit = self.get_month9_visit()
        crfs = self.get_crf_metadata(month9_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_9m_even_if_not_performed_by_6m(self):
        self.get_week2_visit()

        month1_visit = self.get_month1_visit()
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        month3_visit = self.get_month3_visit()
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=NO)

        month6_visit = self.get_month6_visit()
        self.set_mnsi_status(subject_visit=month6_visit, mnsi_performed=NO)

        month9_visit = self.get_month9_visit()
        crfs = self.get_crf_metadata(month9_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_at_12m_even_if_not_performed_by_6m(self):
        self.get_week2_visit()

        month1_visit = self.get_month1_visit()
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=NO)

        month3_visit = self.get_month3_visit()
        self.set_mnsi_status(subject_visit=month3_visit, mnsi_performed=NO)

        month6_visit = self.get_month6_visit()
        self.set_mnsi_status(subject_visit=month6_visit, mnsi_performed=NO)

        self.get_month9_visit()

        month12_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=MONTH12,
            appt_datetime=self.baseline_datetime + relativedelta(months=12),
        )
        crfs = self.get_crf_metadata(month12_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_not_required_between_9m_and_33m(self):
        subject_visit = self.get_visit(visit_code=MONTH6, latest_visit=self.subject_visit)
        for visit_code in [
            MONTH9,
            MONTH12,
            MONTH15,
            MONTH18,
            MONTH21,
            MONTH24,
            MONTH27,
            MONTH30,
        ]:
            with self.subTest(visit_code=visit_code):
                subject_visit = self.get_visit(
                    visit_code=visit_code, latest_visit=subject_visit
                )
                self.assertEqual(subject_visit.visit_code, visit_code)
                self.assertEqual(subject_visit.visit_code_sequence, 0)
                crfs = self.get_crf_metadata(subject_visit)
                self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

    def test_mnsi_required_between_36m_and_45m(self):
        month1_visit = self.get_visit(visit_code=MONTH1, latest_visit=self.subject_visit)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        month36_visit = self.get_visit(visit_code=MONTH36, latest_visit=month1_visit)
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
        self.set_mnsi_status(subject_visit=month42_visit, mnsi_performed=NO)

        month45_visit = self.get_next_subject_visit(month42_visit)
        crfs = self.get_crf_metadata(month45_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.set_mnsi_status(subject_visit=month45_visit, mnsi_performed=NO)

    def test_mnsi_only_required_once_between_36m_and_45m(self):
        month1_visit = self.get_visit(visit_code=MONTH1, latest_visit=self.subject_visit)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        month36_visit = self.get_visit(visit_code=MONTH36, latest_visit=month1_visit)
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

    def test_mnsi_required_at_48m(self):
        month1_visit = self.get_visit(visit_code=MONTH1, latest_visit=self.subject_visit)
        crfs = self.get_crf_metadata(month1_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)

        month3_visit = self.get_next_subject_visit(month1_visit)
        crfs = self.get_crf_metadata(month3_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month36_visit = self.get_visit(visit_code=MONTH36, latest_visit=month3_visit)
        crfs = self.get_crf_metadata(month36_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.set_mnsi_status(subject_visit=month36_visit, mnsi_performed=YES)

        month39_visit = self.get_next_subject_visit(month36_visit)
        crfs = self.get_crf_metadata(month39_visit)
        self.assertNotIn("meta_subject.mnsi", [o.model for o in crfs.all()])

        month48_visit = self.get_visit(visit_code=MONTH48, latest_visit=month39_visit)
        crfs = self.get_crf_metadata(month48_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
