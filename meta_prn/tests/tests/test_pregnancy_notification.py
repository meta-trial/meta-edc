from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from edc_appointment.models import Appointment
from edc_constants.constants import FEMALE, NO, YES
from edc_utils import get_utcnow
from edc_visit_schedule.constants import MONTH1
from model_bakery.baker import make_recipe

from meta_prn.models import OffSchedule
from meta_prn.models.pregnancy_notification import PregnancyNotificationError
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_visit_schedule.constants import SCHEDULE, SCHEDULE_PREGNANCY


class TestPregnancyNotification(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit(gender=FEMALE)

    def test_pregnancy_notification_updates_urine_pregnancy(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)
        urine_pregnancy = make_recipe(
            "meta_subject.urinepregnancy",
            subject_visit=subject_visit,
            report_datetime=get_utcnow(),
            assay_date=get_utcnow().date(),
        )

        self.assertFalse(urine_pregnancy.notified)
        self.assertIsNotNone(urine_pregnancy.assay_date)
        make_recipe(
            "meta_prn.pregnancynotification",
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=get_utcnow(),
        )
        urine_pregnancy.refresh_from_db()
        self.assertTrue(urine_pregnancy.notified)
        self.assertIsNotNone(urine_pregnancy.notified_datetime)

    def test_pregnancy_notification_unconfirmed_ok(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)
        make_recipe(
            "meta_prn.pregnancynotification",
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=get_utcnow(),
            bhcg_confirmed=NO,
            unconfirmed_details="blah blah",
        )

    def test_pregnancy_notification_confirmed_raises(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)
        try:
            make_recipe(
                "meta_prn.pregnancynotification",
                subject_identifier=subject_visit.subject_identifier,
                report_datetime=get_utcnow(),
                bhcg_confirmed=YES,
                unconfirmed_details="blah blah",
            )
        except PregnancyNotificationError:
            pass
        else:
            self.fail("PregnancyNotificationError unexpectedly NOT raised")

    def test_pregnancy_notification_takes_off_schedule(self):

        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)
        make_recipe(
            "meta_prn.pregnancynotification",
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=subject_visit.report_datetime,
            bhcg_confirmed=NO,
            unconfirmed_details="blah blah",
            edd=subject_visit.report_datetime + relativedelta(months=6),
        )

        try:
            OffSchedule.objects.get(subject_identifier=subject_visit.subject_identifier)
        except ObjectDoesNotExist:
            self.fail("OffSchedule unexpectedly does not exist")

        self.assertEqual(Appointment.objects.filter(schedule_name=SCHEDULE).count(), 3)
        self.assertEqual(
            Appointment.objects.filter(schedule_name=SCHEDULE_PREGNANCY).count(), 1
        )
