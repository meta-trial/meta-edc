from django.test import TestCase, tag

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.models import StudyMedication


class TestPhysicalExam(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    @tag("1")
    def test_ok(self):
        StudyMedication(subject_visit=self.subject_visit)
