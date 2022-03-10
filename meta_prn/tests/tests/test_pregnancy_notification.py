from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, override_settings, tag
from edc_action_item.models import ActionItem
from edc_constants.constants import FEMALE
from edc_utils import get_utcnow
from edc_visit_schedule.constants import MONTH1
from model_bakery.baker import make_recipe

from meta_edc.meta_version import PHASE_TWO
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin


@override_settings(META_PHASE=PHASE_TWO)
class TestPregnancyNotification(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit(gender=FEMALE)

    @tag("1")
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
