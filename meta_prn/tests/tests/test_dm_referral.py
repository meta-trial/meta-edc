from django.test import TestCase, tag
from edc_action_item.models import ActionItem
from edc_constants.constants import FEMALE
from edc_utils import get_utcnow
from edc_visit_schedule.constants import MONTH1

from meta_prn.models import DmReferral
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin


class TestDmReferral(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit(gender=FEMALE)

    @tag("1")
    def test_dm_referral(self):
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
        ActionItem.objects.get(
            related_action_item__action_identifier=dm_referral.action_identifier
        )
