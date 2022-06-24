from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from edc_adverse_event.models import AeClassification
from model_bakery import baker

from meta_reports.ae_report import AeReport
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin


class TestReports(MetaTestCaseMixin, TestCase):
    def setUp(self):
        self.user = User.objects.create(username="erikvw", is_staff=True, is_active=True)
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        self.subject_identifier = subject_consent.subject_identifier

    def test_aereport(self):

        rf = RequestFactory()
        request = rf.get("/")
        request.user = self.user
        ae_classification = AeClassification.objects.all()[0]
        ae_initial = baker.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=self.subject_identifier,
            ae_classification=ae_classification,
        )

        report = AeReport(
            ae_initial=ae_initial,
            subject_identifier=ae_initial.subject_identifier,
            user=request.user,
            request=request,
        )
        return report.render()
