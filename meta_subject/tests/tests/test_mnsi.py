from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_constants.constants import NO, YES
from edc_utils import get_utcnow
from model_bakery import baker

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_visit_schedule.constants import MONTH1, MONTH3, MONTH6, MONTH9, MONTH12, WEEK2


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
