"""A throwaway check that migration 0030's conversion does what it says.

Not a migration test: it calls the functions against live models rather
than a migration state, so it says nothing about the graph. It is here
to prove the matching, the reporting and the snapshot re-point behave
on real rows before the migration is run for real.
"""

from importlib import import_module
from io import StringIO
from unittest.mock import patch

from clinicedc_constants import GRADE4, NO, NOT_APPLICABLE, OTHER, YES
from django.db import connection
from django.test import TestCase, override_settings
from edc_adverse_event.models import AeClassification
from model_bakery import baker
from multisite import SiteID

from meta_ae.backfill import backfill_ae_final_classifications
from meta_ae.models import AeFinalClassification, AeInitial, AeTmg
from meta_ae.utils import ae_classification as ae_classification_utils
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin

migration = import_module("meta_ae.migrations.0030_auto_20260916_2111")


class FakeApps:
    """Stand in for the migration state, serving the live models."""

    models = {  # noqa: RUF012
        ("meta_ae", "AeInitial"): AeInitial,
        ("meta_ae", "AeTmg"): AeTmg,
        ("meta_ae", "HistoricalAeInitial"): AeInitial.history.model,
        ("meta_ae", "HistoricalAeTmg"): AeTmg.history.model,
        ("meta_ae", "AeFinalClassification"): AeFinalClassification,
        ("edc_adverse_event", "AeClassification"): AeClassification,
    }

    def get_model(self, app_label, model_name):
        return self.models[(app_label, model_name)]


class FakeSchemaEditor:
    connection = connection


@override_settings(SITE_ID=SiteID(10), EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER=False)
class TestMigration0030(MetaTestCaseMixin, TestCase):
    @staticmethod
    def get_ae_classification(name: str) -> AeClassification:
        return AeClassification.objects.get(name=name)

    def get_ae_initial(self, ae_classification_other: str | None = None) -> AeInitial:
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        return baker.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=subject_consent.subject_identifier,
            ae_grade=GRADE4,
            ae_classification=self.get_ae_classification(OTHER),
            ae_classification_other=ae_classification_other,
        )

    @staticmethod
    def run_conversion() -> str:
        """Call the migration exactly as `migrate` would."""
        out = StringIO()
        with patch.object(ae_classification_utils.sys, "stdout", out):
            migration._update_aeclassification_other_fields(FakeApps(), FakeSchemaEditor())
        return out.getvalue()

    @staticmethod
    def count_rows(ae_classification_other: str) -> int:
        """Live rows plus historical ones, which are converted too."""
        return (
            AeInitial.objects.filter(ae_classification_other=ae_classification_other).count()
            + AeInitial.history.filter(ae_classification_other=ae_classification_other).count()
        )

    def test_it_returns_what_it_did(self):
        """The caller gets the counts, not just the printout."""
        self.get_ae_initial("Anaemia grade 3")
        self.get_ae_initial("Pancreatitis")
        self.get_ae_initial("Renal insufficiency and anaemia")
        recognised = self.count_rows("Anaemia grade 3")
        left = self.count_rows("Pancreatitis") + self.count_rows(
            "Renal insufficiency and anaemia"
        )

        result = ae_classification_utils.update_aeclassification_other_fields()

        self.assertEqual(result.converted, recognised)
        self.assertEqual(result.left_as_other, left)
        self.assertEqual(result.repointed, 0)
        self.assertIn(("AeInitial", "Pancreatitis"), result.unmapped)
        self.assertIn(("AeInitial", "Renal insufficiency and anaemia"), result.ambiguous)

    def test_it_keeps_a_comment_that_is_already_there(self):
        ae_initial = self.get_ae_initial("Anaemia grade 3")
        ae_initial.ae_classification_comment = "reviewed by TMG"
        ae_initial.save()

        self.run_conversion()

        ae_initial.refresh_from_db()
        self.assertEqual(
            ae_initial.ae_classification_comment, "reviewed by TMG; Anaemia grade 3"
        )

    def test_it_converts_free_text_naming_one_classification(self):
        ae_initial = self.get_ae_initial("Anaemia grade 3")

        self.run_conversion()

        ae_initial.refresh_from_db()
        self.assertEqual(ae_initial.ae_classification, self.get_ae_classification("anaemia"))
        self.assertIn(ae_initial.ae_classification_other, [None, ""])

    def test_it_reports_free_text_it_does_not_recognise(self):
        ae_initial = self.get_ae_initial("Pancreatitis")

        out = self.run_conversion()

        ae_initial.refresh_from_db()
        self.assertEqual(ae_initial.ae_classification, self.get_ae_classification(OTHER))
        self.assertIn("nothing recognised", out)
        self.assertIn("Pancreatitis", out)

    def test_it_reports_free_text_naming_more_than_one(self):
        ae_initial = self.get_ae_initial("Renal insufficiency and anaemia")

        out = self.run_conversion()

        ae_initial.refresh_from_db()
        self.assertEqual(ae_initial.ae_classification, self.get_ae_classification(OTHER))
        self.assertIn("names more than one", out)

    def test_it_converts_the_tmg_investigator_classification(self):
        ae_initial = self.get_ae_initial("Anaemia")
        ae_tmg = baker.make_recipe(
            "meta_ae.aetmg",
            ae_initial=ae_initial,
            subject_identifier=ae_initial.subject_identifier,
            original_report_agreed=NO,
            investigator_ae_classification=self.get_ae_classification(OTHER),
            investigator_ae_classification_other="Thrombocytopenia grade 4",
        )

        self.run_conversion()

        ae_tmg.refresh_from_db()
        self.assertEqual(
            ae_tmg.investigator_ae_classification,
            self.get_ae_classification("thrombocytopenia"),
        )

    def test_a_settled_record_stays_settled(self):
        """The snapshot follows the source it was taken from."""
        ae_initial = self.get_ae_initial("Anaemia")
        baker.make_recipe(
            "meta_ae.aetmg",
            ae_initial=ae_initial,
            subject_identifier=ae_initial.subject_identifier,
            original_report_agreed=YES,
            investigator_ae_classification=self.get_ae_classification(NOT_APPLICABLE),
        )
        backfill_ae_final_classifications(AeInitial.objects.all())
        obj = AeFinalClassification.objects.get()
        obj.final_ae_classification = self.get_ae_classification("anaemia")
        obj.conflict_resolved = YES
        obj.save()
        self.assertEqual(obj.resolved_ae_classification, self.get_ae_classification(OTHER))

        out = self.run_conversion()

        obj.refresh_from_db()
        self.assertEqual(obj.resolved_ae_classification, self.get_ae_classification("anaemia"))
        self.assertIn("Re-pointed 1 resolved", out)

    def test_an_unsettled_record_is_left_for_the_backfill(self):
        ae_initial = self.get_ae_initial("Anaemia")
        backfill_ae_final_classifications(AeInitial.objects.all())

        out = self.run_conversion()

        obj = AeFinalClassification.objects.get()
        self.assertIsNone(obj.resolved_ae_classification)
        self.assertIn("Re-pointed 0 resolved", out)
        self.assertEqual(ae_initial.subject_identifier, obj.subject_identifier)
