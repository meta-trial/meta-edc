from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, override_settings, tag
from edc_action_item.models import ActionItem
from edc_utils import get_utcnow
from edc_visit_schedule.constants import MONTH1
from model_bakery.baker import make_recipe

from meta_edc.meta_version import PHASE_TWO
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin


@override_settings(META_PHASE=PHASE_TWO)
class TestMetadataRules(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()
        self.data = dict(
            subject_visit=self.subject_visit.pk,
            report_datetime=self.subject_visit.report_datetime,
        )

    @tag("1")
    def test_pregnancy_actions(self):
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
            self.fail(
                "ActionItem for pregnancynotification unexpectedly does not exist"
            )

        pregnancy_notification = make_recipe(
            "meta_prn.pregnancynotification",
            subject_identifier=subject_visit.subject_identifier,
        )

        try:
            ActionItem.objects.get(
                parent_action_item__action_identifier=pregnancy_notification.action_identifier,
                reference_model="meta_prn.delivery",
            )
        except ObjectDoesNotExist:
            self.fail("ActionItem for delivery unexpectedly does not exist")

        try:
            ActionItem.objects.get(
                parent_action_item__action_identifier=pregnancy_notification.action_identifier,
                reference_model="meta_prn.delivery",
            )
        except ObjectDoesNotExist:
            self.fail("ActionItem for delivery unexpectedly does not exist")

        delivery = make_recipe(
            "meta_prn.delivery",
            subject_identifier=subject_visit.subject_identifier,
        )

        birth_outcomes = make_recipe(
            "meta_prn.birthoutcomes",
            subject_identifier=subject_visit.subject_identifier,
            delivery=delivery,
        )
