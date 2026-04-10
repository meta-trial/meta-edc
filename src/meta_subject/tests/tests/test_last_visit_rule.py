from datetime import datetime
from zoneinfo import ZoneInfo

import time_machine
from clinicedc_constants import YES
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, override_settings, tag
from django.utils import timezone
from model_bakery import baker

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.models import SubjectVisit
from meta_visit_schedule.constants import MONTH1, MONTH36, MONTH39, MONTH42, MONTH45, MONTH48


@override_settings(
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=datetime(2019, 1, 1, 0, 0, tzinfo=ZoneInfo("UTC")),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=datetime(2028, 12, 31, 0, 0, tzinfo=ZoneInfo("UTC")),
    SITE_ID=10,
)
class TestLastVisitRuleGroup2(MetaTestCaseMixin, TestCase):
    """Confirm CRFs are added to the `last` visit.

    Study ends abruptly on June 1. Assume any visit after 01 MAR 2026
    is the subject's last. Require the 48M CRFs at this visit.
    """

    def setUp(self):
        super().setUp()
        baseline_dt = datetime(2023, 4, 1, 8, 0, tzinfo=ZoneInfo("UTC"))
        traveller = time_machine.travel(baseline_dt)
        traveller.start()
        subject_screening = self.get_subject_screening(
            report_datetime=timezone.now(),
            eligibility_datetime=timezone.now(),
        )
        self.subject_consent = self.get_subject_consent(
            subject_screening, consent_datetime=timezone.now()
        )

        self.subject_visit = self.get_subject_visit(
            subject_screening=subject_screening,
            subject_consent=self.subject_consent,
            appt_datetime=timezone.now(),
        )
        traveller.stop()

        # add consent extension which has a start date of 16/12/2024
        # this adds the appointments after MONTH36
        consent_v1_ext_start_dt = datetime(2024, 12, 16, tzinfo=ZoneInfo("UTC"))
        traveller = time_machine.travel(consent_v1_ext_start_dt)
        traveller.start()
        self.get_subject_consent_extended(
            self.subject_consent, consent_datetime=timezone.now()
        )
        traveller.stop()

    def get_visit(self, visit_code: str):
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
        return subject_visit

    @staticmethod
    def set_mnsi_status(subject_visit, mnsi_performed):
        baker.make(
            "meta_subject.mnsi",
            report_datetime=subject_visit.report_datetime,
            subject_visit=subject_visit,
            mnsi_performed=mnsi_performed,
        )

    @tag("1")
    def test_mnsi_required_at_all_last_visits_after_march_2026_36(self):
        """MNSI required at MONTH36+ even after mnsi_performed=YES at each visit,
        because all visits fall after 2026-03-01 (LastVisitRuleGroup)."""
        month1_visit = self.get_visit(MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)
        subject_visit = self.get_visit(MONTH36)
        self.assertGreaterEqual(
            subject_visit.report_datetime,
            datetime(2026, 3, 1, 0, 0, tzinfo=ZoneInfo("UTC")),
        )
        crfs = self.get_crf_metadata(subject_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.assertIn("meta_subject.glucose", [o.model for o in crfs.all()])

    @tag("1")
    def test_mnsi_required_at_all_last_visits_after_march_2026_39(self):
        month1_visit = self.get_visit(MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)
        subject_visit = self.get_visit(MONTH39)
        self.assertGreaterEqual(
            subject_visit.report_datetime,
            datetime(2026, 3, 1, 0, 0, tzinfo=ZoneInfo("UTC")),
        )
        crfs = self.get_crf_metadata(subject_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.assertIn("meta_subject.glucose", [o.model for o in crfs.all()])

    @tag("1")
    def test_mnsi_required_at_all_last_visits_after_march_2026_42(self):
        month1_visit = self.get_visit(MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)
        subject_visit = self.get_visit(MONTH42)
        self.assertGreaterEqual(
            subject_visit.report_datetime,
            datetime(2026, 3, 1, 0, 0, tzinfo=ZoneInfo("UTC")),
        )
        crfs = self.get_crf_metadata(subject_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.assertIn("meta_subject.glucose", [o.model for o in crfs.all()])

    @tag("1")
    def test_mnsi_required_at_all_last_visits_after_march_2026_45(self):
        month1_visit = self.get_visit(MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)
        subject_visit = self.get_visit(MONTH45)
        self.assertGreaterEqual(
            subject_visit.report_datetime,
            datetime(2026, 3, 1, 0, 0, tzinfo=ZoneInfo("UTC")),
        )
        crfs = self.get_crf_metadata(subject_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.assertIn("meta_subject.glucose", [o.model for o in crfs.all()])

    @tag("1")
    def test_mnsi_required_at_all_last_visits_after_march_2026_48(self):
        month1_visit = self.get_visit(MONTH1)
        self.set_mnsi_status(subject_visit=month1_visit, mnsi_performed=YES)
        subject_visit = self.get_visit(MONTH48)
        self.assertGreaterEqual(
            subject_visit.report_datetime,
            datetime(2026, 3, 1, 0, 0, tzinfo=ZoneInfo("UTC")),
        )
        crfs = self.get_crf_metadata(subject_visit)
        self.assertIn("meta_subject.mnsi", [o.model for o in crfs.all()])
        self.assertIn("meta_subject.glucose", [o.model for o in crfs.all()])
