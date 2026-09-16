"""Tests for the "Refresh from the source reports" admin action.

The action is the admin face of `backfill_ae_final_classification
--update-copies`, so what it does to a record is covered by the command
tests. What is covered here is what only the action can get wrong: the
records it reaches, and what it tells the person who ran it.
"""

from clinicedc_constants import GRADE4, NO, YES
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase, override_settings
from edc_adverse_event.models import AeClassification
from model_bakery import baker
from multisite import SiteID

from meta_ae.admin.actions import refresh_ae_final_classification
from meta_ae.backfill import backfill_ae_final_classifications
from meta_ae.models import AeFinalClassification, AeInitial
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin

LACTIC_ACIDOSIS = "lactic_acidosis"
HEPATOMEGALY = "hepatomegaly_steatosis"


@override_settings(SITE_ID=SiteID(10), EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER=False)
class TestRefreshAeFinalClassificationAction(MetaTestCaseMixin, TestCase):
    @staticmethod
    def get_ae_classification(name: str) -> AeClassification:
        return AeClassification.objects.get(name=name)

    def get_ae_initial(self) -> AeInitial:
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        return baker.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=subject_consent.subject_identifier,
            ae_grade=GRADE4,
            ae_classification=self.get_ae_classification(LACTIC_ACIDOSIS),
        )

    def get_ae_tmg(self, ae_initial: AeInitial, original_report_agreed: str = YES):
        return baker.make_recipe(
            "meta_ae.aetmg",
            ae_initial=ae_initial,
            subject_identifier=ae_initial.subject_identifier,
            original_report_agreed=original_report_agreed,
        )

    @staticmethod
    def run_action(queryset) -> list[str]:
        """Run the action and return what it told the user."""
        request = RequestFactory().get("/")
        request.session = "session"
        request._messages = FallbackStorage(request)
        refresh_ae_final_classification(None, request, queryset)
        return [str(message) for message in get_messages(request)]

    def test_the_action_refreshes_only_the_selected_records(self):
        selected_ae_initial = self.get_ae_initial()
        other_ae_initial = self.get_ae_initial()
        backfill_ae_final_classifications(AeInitial.objects.all())
        self.get_ae_tmg(selected_ae_initial)
        self.get_ae_tmg(other_ae_initial)

        self.run_action(AeFinalClassification.objects.filter(ae_initial=selected_ae_initial))

        selected = AeFinalClassification.objects.get(ae_initial=selected_ae_initial)
        other = AeFinalClassification.objects.get(ae_initial=other_ae_initial)
        self.assertIsNotNone(selected.ae_tmg)
        self.assertIsNone(other.ae_tmg)

    def test_the_action_reports_what_it_refreshed(self):
        ae_initial = self.get_ae_initial()
        backfill_ae_final_classifications(AeInitial.objects.all())
        self.get_ae_tmg(ae_initial)

        messages = self.run_action(AeFinalClassification.objects.all())

        self.assertIn("Refreshed 1/1", messages[0])

    def test_the_action_says_nothing_was_needed(self):
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        backfill_ae_final_classifications(AeInitial.objects.all())

        messages = self.run_action(AeFinalClassification.objects.all())

        self.assertIn("Refreshed 0/1", messages[0])
        self.assertIn("1 already current", messages[0])

    def test_the_action_names_the_settled_records_it_left_alone(self):
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        backfill_ae_final_classifications(AeInitial.objects.all())
        obj = AeFinalClassification.objects.get()
        obj.conflict_resolved = YES
        obj.save()
        ae_tmg.original_report_agreed = NO
        ae_tmg.investigator_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_tmg.save()

        messages = self.run_action(AeFinalClassification.objects.all())

        self.assertIn("Left 1 resolved record(s) unchanged", messages[-1])
        self.assertIn(ae_initial.subject_identifier, messages[-1])
        obj.refresh_from_db()
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )

    def test_the_action_stays_quiet_when_nothing_was_left_alone(self):
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        backfill_ae_final_classifications(AeInitial.objects.all())

        messages = self.run_action(AeFinalClassification.objects.all())

        self.assertEqual(len(messages), 1)
