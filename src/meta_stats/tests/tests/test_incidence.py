from clinicedc_constants import FEMALE
from django.test import TestCase

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin


class TestIncidence(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit(gender=FEMALE)
