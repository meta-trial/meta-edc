from django.test import TestCase, override_settings
from model_bakery.baker import make_recipe

from meta_edc.meta_version import PHASE_TWO
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.forms import FollowupExaminationForm


@override_settings(META_PHASE=PHASE_TWO)
class TestMetadataRules(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()
        self.data = dict(
            subject_visit=self.subject_visit.pk,
            report_datetime=self.subject_visit.report_datetime,
        )

    def test_ok(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        obj = make_recipe(
            "meta_subject.followupexamination", subject_visit=subject_visit
        )
        form = FollowupExaminationForm(instance=obj)
        form.is_valid()
