from django.test import TestCase, override_settings, tag
from edc_constants.constants import FEMALE, MALE
from edc_utils import get_utcnow
from edc_visit_schedule.constants import MONTH1
from model_bakery.baker import make_recipe

from meta_edc.meta_version import PHASE_TWO
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.forms import FollowupExaminationForm


@override_settings(META_PHASE=PHASE_TWO)
class TestMetadataRules(MetaTestCaseMixin, TestCase):
    def test_ok(self):
        self.subject_visit = self.get_subject_visit(gender=FEMALE)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        obj = make_recipe(
            "meta_subject.followupexamination", subject_visit=subject_visit
        )
        form = FollowupExaminationForm(instance=obj)
        form.is_valid()

    @tag("1")
    def test_pregnancy_not_required_for_male(self):
        self.subject_visit = self.get_subject_visit(gender=MALE)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)

        self.assertNotIn(
            "meta_subject.urinepregnancy",
            [obj.model for obj in self.get_crf_metadata(subject_visit)],
        )

        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertNotIn(
            "meta_subject.urinepregnancy",
            [obj.model for obj in self.get_crf_metadata(subject_visit)],
        )

    @tag("1")
    def test_pregnancy_required_for_female(self):
        self.subject_visit = self.get_subject_visit(gender=FEMALE)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)

        self.assertIn(
            "meta_subject.urinepregnancy",
            [obj.model for obj in self.get_crf_metadata(subject_visit)],
        )

        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertIn(
            "meta_subject.urinepregnancy",
            [obj.model for obj in self.get_crf_metadata(subject_visit)],
        )

    @tag("1")
    def test_pregnancy_required_for_female(self):
        self.subject_visit = self.get_subject_visit(gender=FEMALE)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        urine_pregnancy = make_recipe(
            "meta_subject.urinepregnancy",
            subject_visit=subject_visit,
            report_datetime=get_utcnow(),
            assay_date=get_utcnow().date(),
        )
        self.assertFalse(urine_pregnancy.notified)
        self.assertIsNone(urine_pregnancy.notified_datetime)
        self.assertEqual(
            subject_visit.subject_identifier,
            urine_pregnancy.subject_visit.subject_identifier,
        )
        make_recipe(
            "meta_prn.pregnancynotification",
            subject_identifier=subject_visit.subject_identifier,
        )
