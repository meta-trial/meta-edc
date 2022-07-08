from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from edc_action_item.models import ActionItem
from edc_appointment.models import Appointment
from edc_constants.constants import FEMALE
from edc_utils import get_utcnow
from edc_visit_schedule.constants import MONTH1
from model_bakery.baker import make_recipe

from meta_prn.models import OffSchedulePregnancy
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_visit_schedule.constants import DELIVERY


class TestMetadataRules(MetaTestCaseMixin, TestCase):
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

    def test_pregnancy_actions(self):  # noqa
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)

        urine_pregnancy = make_recipe(
            "meta_subject.urinepregnancy",
            subject_visit=subject_visit,
            report_datetime=get_utcnow(),
            assay_date=get_utcnow().date(),
        )

        try:
            ActionItem.objects.get(
                action_identifier=urine_pregnancy.action_identifier,
                reference_model="meta_subject.urinepregnancy",
            )
        except ObjectDoesNotExist:
            self.fail("ActionItem for urinepregnancy unexpectedly does not exist")

        try:
            ActionItem.objects.get(
                parent_action_item__action_identifier=urine_pregnancy.action_identifier,
                reference_model="meta_prn.pregnancynotification",
            )
        except ObjectDoesNotExist:
            self.fail("ActionItem for pregnancynotification unexpectedly does not exist")

        make_recipe(
            "meta_prn.pregnancynotification",
            subject_identifier=subject_visit.subject_identifier,
        )

        try:
            appointment = Appointment.objects.get(visit_code=DELIVERY)
        except ObjectDoesNotExist:
            self.fail("delivery appointment unexpectedly does not exist")

        subject_visit = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
            visit_code=DELIVERY,
            visit_code_sequence=0,
            appt_datetime=appointment.appt_datetime,
        )

        delivery = make_recipe(
            "meta_subject.delivery",
            subject_visit=subject_visit,
        )

        try:
            ActionItem.objects.get(
                parent_action_item__action_identifier=delivery.action_identifier,
                reference_model="meta_prn.offschedulepregnancy",
            )
        except ObjectDoesNotExist:
            self.fail("ActionItem for offschedulepregnancy unexpectedly does not exist")

        offschedule_pregancy = OffSchedulePregnancy.objects.get(
            subject_identifier=delivery.subject_visit.subject_identifier
        )
        try:
            ActionItem.objects.get(
                parent_action_item__action_identifier=offschedule_pregancy.action_identifier,
                reference_model="meta_prn.endofstudy",
            )
        except ObjectDoesNotExist:
            self.fail("ActionItem for endofstudy unexpectedly does not exist")
