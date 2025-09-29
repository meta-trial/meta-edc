from django.test import TestCase

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin


class TestSubjectConsent(MetaTestCaseMixin, TestCase):
    def test_(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        self.assertIsNotNone(subject_consent.subject_identifier)
