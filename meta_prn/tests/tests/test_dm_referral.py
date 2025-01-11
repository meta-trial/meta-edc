from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from edc_action_item.models import ActionItem
from edc_appointment.constants import COMPLETE_APPT
from edc_appointment.models import Appointment
from edc_constants.constants import CLOSED, FEMALE, NEW, NO, PATIENT, YES
from edc_pharmacy.constants import IN_PROGRESS_APPT
from edc_utils import get_utcnow
from edc_visit_schedule.constants import MONTH1, OFFSCHEDULE_ACTION
from edc_visit_tracking.constants import SCHEDULED

from meta_lists.models import MissedReferralReasons
from meta_prn.constants import (
    OFFSCHEDULE_DM_REFERRAL_ACTION,
    OFFSTUDY_MEDICATION_ACTION,
)
from meta_prn.models import DmReferral, OnScheduleDmReferral
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.constants import DM_FOLLOWUP_ACTION
from meta_subject.models import DmEndpoint, DmFollowup, SubjectVisit
from meta_visit_schedule.constants import DM_BASELINE, DM_FOLLOWUP, SCHEDULE_DM_REFERRAL


class TestDmReferral(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit(gender=FEMALE)

    def test_dm_referral_puts_subject_on_dm_followup_schedule(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)
        dm_referral = DmReferral.objects.create(
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=get_utcnow(),
            referral_date=get_utcnow(),
        )
        self.assertIsNotNone(dm_referral.report_datetime)
        self.assertIsNotNone(dm_referral.referral_date)
        self.assertIsNotNone(dm_referral.action_identifier)

        # verify subject is on DM Followup schedule
        try:
            OnScheduleDmReferral.objects.get(
                subject_identifier=subject_visit.subject_identifier
            )
        except ObjectDoesNotExist:
            self.fail("OnScheduleDmReferral unexpectedly does not exist")

    def test_dm_referral_action_creates_offschedule_action(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)
        dm_referral = DmReferral.objects.create(
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=get_utcnow(),
            referral_date=get_utcnow(),
        )
        self.assertIsNotNone(dm_referral.report_datetime)
        self.assertIsNotNone(dm_referral.referral_date)
        self.assertIsNotNone(dm_referral.action_identifier)

        try:
            ActionItem.objects.get(
                subject_identifier=subject_visit.subject_identifier,
                action_type__name=OFFSCHEDULE_ACTION,
                status=CLOSED,
            )
        except ObjectDoesNotExist:
            self.fail(f"{OFFSCHEDULE_ACTION} Action item unexpectedly does not exist")

    def test_dm_referral_creates_offstudy_med_action(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)
        dm_referral = DmReferral.objects.create(
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=get_utcnow(),
            referral_date=get_utcnow(),
        )
        self.assertIsNotNone(dm_referral.report_datetime)
        self.assertIsNotNone(dm_referral.referral_date)
        self.assertIsNotNone(dm_referral.action_identifier)

        # verify action items are created
        try:
            ActionItem.objects.get(
                subject_identifier=subject_visit.subject_identifier,
                action_type__name=OFFSTUDY_MEDICATION_ACTION,
                status=NEW,
            )
        except ObjectDoesNotExist:
            self.fail(f"{OFFSTUDY_MEDICATION_ACTION} Action item unexpectedly does not exist")

    def test_dm_referral_creates_dm_followup_action(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)
        dm_referral = DmReferral.objects.create(
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=get_utcnow(),
            referral_date=get_utcnow(),
        )
        self.assertIsNotNone(dm_referral.report_datetime)
        self.assertIsNotNone(dm_referral.referral_date)
        self.assertIsNotNone(dm_referral.action_identifier)

        try:
            ActionItem.objects.get(
                subject_identifier=subject_visit.subject_identifier,
                action_type__name=DM_FOLLOWUP_ACTION,
                status=NEW,
            )
        except ObjectDoesNotExist:
            self.fail(f"{DM_FOLLOWUP_ACTION} Action item unexpectedly does not exist")

    def test_dm_referral2(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)
        referral_datetime = subject_visit.report_datetime
        DmReferral.objects.create(
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=referral_datetime,
            referral_date=referral_datetime.date(),
        )

        # Add DM Baseline
        appointment = Appointment.objects.get(
            subject_identifier=subject_visit.subject_identifier,
            schedule_name=SCHEDULE_DM_REFERRAL,
            visit_code=DM_BASELINE,
        )
        appointment.appt_status = IN_PROGRESS_APPT
        appointment.save()

        subject_visit = SubjectVisit.objects.create(
            appointment=appointment,
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=appointment.appt_datetime,
            reason=SCHEDULED,
            info_source=PATIENT,
        )

        DmEndpoint.objects.create(
            subject_visit=subject_visit,
            report_datetime=get_utcnow(),
            dx_date=referral_datetime.date(),
            dx_initiated_by="fbg_confirmed",
            dx_tmg=YES,
            dx_tmg_date=referral_datetime.date(),
        )

        # Add DM Followup
        followup_datetime = referral_datetime + relativedelta(months=6)
        appointment = Appointment.objects.get(
            subject_identifier=subject_visit.subject_identifier,
            schedule_name=SCHEDULE_DM_REFERRAL,
            visit_code=DM_FOLLOWUP,
        )
        appointment.appt_status = IN_PROGRESS_APPT
        appointment.save()

        subject_visit = SubjectVisit.objects.create(
            appointment=appointment,
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=appointment.appt_datetime,
            reason=SCHEDULED,
            info_source=PATIENT,
        )

        dm_followup = DmFollowup.objects.create(
            subject_visit=subject_visit,
            report_datetime=followup_datetime,
            referral_date=referral_datetime.date(),
            attended=NO,
            on_dm_medications=NO,
        )
        dm_followup.missed_referral_reasons.set([MissedReferralReasons.objects.all()[0]])

        appointment.appt_status = COMPLETE_APPT
        appointment.save()

        try:
            ActionItem.objects.get(
                subject_identifier=subject_visit.subject_identifier,
                action_type__name=DM_FOLLOWUP_ACTION,
                status=CLOSED,
            )
        except ObjectDoesNotExist:
            self.fail(f"{DM_FOLLOWUP_ACTION} Action item unexpectedly does not exist")

        try:
            ActionItem.objects.get(
                subject_identifier=subject_visit.subject_identifier,
                action_type__name=OFFSCHEDULE_DM_REFERRAL_ACTION,
                status=NEW,
            )
        except ObjectDoesNotExist:
            self.fail(
                f"{OFFSCHEDULE_DM_REFERRAL_ACTION} Action item unexpectedly does not exist"
            )
