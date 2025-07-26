from django.test import TestCase
from edc_action_item.models import ActionItem
from edc_constants.constants import FEMALE, NEW, PATIENT, YES
from edc_offstudy.constants import END_OF_STUDY_ACTION
from edc_pharmacy.models import Medication
from edc_transfer.constants import SUBJECT_TRANSFER_ACTION, TRANSFERRED
from edc_utils import get_utcnow
from edc_visit_schedule.constants import OFFSCHEDULE_ACTION

from meta_lists.models import OffstudyReasons, TransferReasons
from meta_pharmacy.constants import METFORMIN
from meta_prn.action_items import OffscheduleAction, SubjectTransferAction
from meta_prn.constants import OFFSTUDY_MEDICATION_ACTION
from meta_prn.models import EndOfStudy, OffSchedule, OffStudyMedication, SubjectTransfer
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin


class TestEosEvents(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_screening = self.get_subject_screening(gender=FEMALE)
        self.subject_consent = self.get_subject_consent(self.subject_screening)
        self.subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
        )
        self.data = dict(
            subject_visit=self.subject_visit.pk,
            report_datetime=self.subject_visit.report_datetime,
        )

    def test_transfer_to_offschedule_in_order(self):
        SubjectTransferAction(
            subject_identifier=self.subject_consent.subject_identifier,
            skip_get_current_site=True,
            site_id=self.subject_consent.site_id,
        )
        action_types = [
            obj.action_type.name
            for obj in ActionItem.objects.filter(status=NEW).order_by("action_type__name")
        ]
        self.assertEqual(action_types, [SUBJECT_TRANSFER_ACTION])

        # add a subject transfer object, which triggers next action item
        transfer_reason = TransferReasons.objects.get(name="moved")
        subject_transfer = SubjectTransfer.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            initiated_by="patient",
            may_return=YES,
            may_contact=YES,
        )
        subject_transfer.transfer_reason.add(transfer_reason)

        action_types = [
            obj.action_type.name
            for obj in ActionItem.objects.filter(status=NEW).order_by("action_type__name")
        ]
        self.assertEqual(action_types, [OFFSCHEDULE_ACTION, OFFSTUDY_MEDICATION_ACTION])

        OffSchedule.objects.create(subject_identifier=self.subject_consent.subject_identifier)

        action_types = [
            obj.action_type.name
            for obj in ActionItem.objects.filter(status=NEW).order_by("action_type__name")
        ]
        self.assertEqual(action_types, [OFFSTUDY_MEDICATION_ACTION])

        offstudy_rx = OffStudyMedication.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            stop_date=get_utcnow().date(),
            last_dose_date=get_utcnow().date(),
            reason=PATIENT,
        )
        offstudy_rx.medications.add(Medication.objects.get(name=METFORMIN))

        action_types = [
            obj.action_type.name
            for obj in ActionItem.objects.filter(status=NEW).order_by("action_type__name")
        ]
        self.assertEqual(action_types, [END_OF_STUDY_ACTION])

        EndOfStudy.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            last_seen_date=get_utcnow().date(),
            offstudy_reason=OffstudyReasons.objects.get(name=TRANSFERRED),
        )

        action_types = [
            obj.action_type.name
            for obj in ActionItem.objects.filter(status=NEW).order_by("action_type__name")
        ]
        self.assertEqual(action_types, [])

    def test_transfer_to_offschedule_raises(self):

        OffscheduleAction(
            subject_identifier=self.subject_consent.subject_identifier,
            skip_get_current_site=True,
            site_id=self.subject_consent.site_id,
        )

        OffSchedule.objects.create(subject_identifier=self.subject_consent.subject_identifier)

        action_types = [
            obj.action_type.name
            for obj in ActionItem.objects.filter(status=NEW).order_by("action_type__name")
        ]
        self.assertEqual(action_types, [OFFSTUDY_MEDICATION_ACTION])

        offstudy_rx = OffStudyMedication.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            stop_date=get_utcnow().date(),
            last_dose_date=get_utcnow().date(),
            reason=PATIENT,
        )
        offstudy_rx.medications.add(Medication.objects.get(name=METFORMIN))

        action_types = [
            obj.action_type.name
            for obj in ActionItem.objects.filter(status=NEW).order_by("action_type__name")
        ]
        self.assertEqual(action_types, [END_OF_STUDY_ACTION])

        EndOfStudy.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            last_seen_date=get_utcnow().date(),
            offstudy_reason=OffstudyReasons.objects.get(name=TRANSFERRED),
        )

        action_types = [
            obj.action_type.name
            for obj in ActionItem.objects.filter(status=NEW).order_by("action_type__name")
        ]
        self.assertEqual(action_types, [])
