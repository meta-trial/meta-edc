"""Tests documenting the rerun behaviour of `backfill_ae_final_classification`.

Some of these tests are expected to fail against the current
implementation; they pin down the caveats before any fix is written:

* `refresh_copies_from_sources` copies the AeTmg columns onto an
  existing row but never applies the agreement/autofill logic, so a row
  created before its AeTmg existed is left with a null
  `final_ae_classification` even once the sources agree.
* `Command.get_ae_tmg` suppresses only `DoesNotExist`, so a second
  AeTmg on the same AeInitial (allowed: `AeTmgAction` is not a
  singleton and lists itself as a parent action) aborts the whole run.
* `refresh_copies_from_sources` ignores `verified`: it clears
  `final_ae_classification` on any source classification change, so a
  verified row loses its agreed answer. `verified` is meant to protect
  `final_ae_classification` from further change by the command; the
  copied columns still refresh.
"""

from io import StringIO

from clinicedc_constants import GRADE4, NO, YES
from django.core.management import call_command
from django.test import TestCase, override_settings
from edc_adverse_event.models import AeClassification
from model_bakery import baker
from multisite import SiteID

from meta_ae.models import AeFinalClassification, AeInitial, AeTmg
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin

LACTIC_ACIDOSIS = "lactic_acidosis"
HEPATOMEGALY = "hepatomegaly_steatosis"


@override_settings(SITE_ID=SiteID(10), EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER=False)
class TestBackfillAeFinalClassification(MetaTestCaseMixin, TestCase):
    @staticmethod
    def get_ae_classification(name: str) -> AeClassification:
        return AeClassification.objects.get(name=name)

    def get_ae_initial(self, classification_name: str = LACTIC_ACIDOSIS) -> AeInitial:
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        return baker.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=subject_consent.subject_identifier,
            ae_grade=GRADE4,
            ae_classification=self.get_ae_classification(classification_name),
        )

    def get_ae_tmg(
        self,
        ae_initial: AeInitial,
        classification_name: str = LACTIC_ACIDOSIS,
        original_report_agreed: str = YES,
    ) -> AeTmg:
        return baker.make_recipe(
            "meta_ae.aetmg",
            ae_initial=ae_initial,
            subject_identifier=ae_initial.subject_identifier,
            original_report_agreed=original_report_agreed,
            investigator_ae_classification=self.get_ae_classification(classification_name),
        )

    @staticmethod
    def backfill(**kwargs) -> str:
        out = StringIO()
        call_command("backfill_ae_final_classification", stdout=out, **kwargs)
        return out.getvalue()

    # ------------------------------------------------------------------
    # baseline: rerunning with no flags is a no-op
    # ------------------------------------------------------------------
    def test_rerun_without_flags_creates_nothing_the_second_time(self):
        self.get_ae_initial()
        self.backfill()
        self.assertEqual(AeFinalClassification.objects.count(), 1)
        obj = AeFinalClassification.objects.get()
        modified = obj.modified

        self.backfill()

        self.assertEqual(AeFinalClassification.objects.count(), 1)
        obj.refresh_from_db()
        self.assertEqual(obj.modified, modified)

    def test_rerun_without_flags_ignores_an_ae_tmg_added_since_the_last_run(self):
        """Without --update-copies a new AeTmg is invisible to a rerun."""
        ae_initial = self.get_ae_initial()
        self.backfill()
        self.get_ae_tmg(ae_initial)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertIsNone(obj.ae_tmg)
        self.assertIsNone(obj.investigator_ae_classification)

    # ------------------------------------------------------------------
    # control: the create path does autofill when the AeTmg is present
    # ------------------------------------------------------------------
    def test_create_path_autofills_final_classification_when_sources_agree(self):
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )
        self.assertTrue(obj.verified)

    # ------------------------------------------------------------------
    # --update-copies picks up a new AeTmg ...
    # ------------------------------------------------------------------
    def test_update_copies_picks_up_an_ae_tmg_added_since_the_last_run(self):
        ae_initial = self.get_ae_initial()
        self.backfill()
        ae_tmg = self.get_ae_tmg(ae_initial)

        self.backfill(update_copies=True)

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.ae_tmg, ae_tmg)
        self.assertEqual(obj.ae_tmg_action_identifier, ae_tmg.action_identifier)
        self.assertEqual(
            obj.investigator_ae_classification,
            self.get_ae_classification(LACTIC_ACIDOSIS),
        )
        self.assertEqual(obj.investigator_ae_classification_agreed, YES)

    # ------------------------------------------------------------------
    # ... but does not autofill, unlike the create path (expected failure)
    # ------------------------------------------------------------------
    def test_update_copies_autofills_final_classification_when_tmg_added_later(self):
        """Same data as the create-path control, different result.

        A row backfilled before its AeTmg existed should end up
        equivalent to one backfilled after, once --update-copies has
        refreshed it.
        """
        ae_initial = self.get_ae_initial()
        self.backfill()
        self.get_ae_tmg(ae_initial)

        self.backfill(update_copies=True)

        obj = AeFinalClassification.objects.get()
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )
        self.assertTrue(obj.verified)

    def test_update_copies_restores_final_classification_cleared_by_a_new_tmg(self):
        """An investigator-entered value is cleared when the AeTmg lands.

        Clearing is correct when the sources disagree, but here the
        arriving AeTmg agrees with the investigator, so the refresh
        should leave an agreed value in place rather than a null.
        """
        ae_initial = self.get_ae_initial()
        self.backfill()
        obj = AeFinalClassification.objects.get()
        obj.final_ae_classification = self.get_ae_classification(LACTIC_ACIDOSIS)
        obj.save(update_fields=["final_ae_classification"])
        self.get_ae_tmg(ae_initial)

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )

    def test_update_copies_clears_final_classification_when_new_tmg_disagrees(self):
        """Clearing on disagreement is the intended behaviour.

        The row is not verified, so `final_ae_classification` is still
        the command's to revise.
        """
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        self.backfill()
        obj = AeFinalClassification.objects.get()
        self.assertFalse(obj.verified)
        obj.final_ae_classification = self.get_ae_classification(LACTIC_ACIDOSIS)
        obj.save(update_fields=["final_ae_classification"])
        self.get_ae_tmg(ae_initial, HEPATOMEGALY, original_report_agreed=NO)

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertIsNone(obj.final_ae_classification)
        self.assertFalse(obj.verified)

    # ------------------------------------------------------------------
    # verified rows are protected from further change (expected failure)
    # ------------------------------------------------------------------
    def test_update_copies_leaves_verified_final_classification_when_tmg_changes(self):
        """`verified` freezes `final_ae_classification`.

        The copied columns must still refresh so the row shows what the
        sources now say, but the agreed answer is not the command's to
        revise once it is verified.
        """
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        self.backfill()
        obj = AeFinalClassification.objects.get()
        self.assertTrue(obj.verified)
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )

        ae_tmg.investigator_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_tmg.original_report_agreed = NO
        ae_tmg.save()

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )
        self.assertTrue(obj.verified)
        self.assertEqual(
            obj.investigator_ae_classification, self.get_ae_classification(HEPATOMEGALY)
        )
        self.assertEqual(obj.investigator_ae_classification_agreed, NO)

    def test_update_copies_leaves_verified_final_classification_when_ae_initial_changes(
        self,
    ):
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        self.backfill()
        obj = AeFinalClassification.objects.get()
        self.assertTrue(obj.verified)

        ae_initial.ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_initial.save()

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )
        self.assertTrue(obj.verified)
        self.assertEqual(obj.ae_classification, self.get_ae_classification(HEPATOMEGALY))

    def test_update_copies_leaves_verified_final_classification_when_tmg_added_later(self):
        """A verified row predating its AeTmg keeps its agreed answer."""
        ae_initial = self.get_ae_initial()
        self.backfill()
        obj = AeFinalClassification.objects.get()
        obj.final_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        obj.verified = True
        obj.save(update_fields=["final_ae_classification", "verified"])
        self.get_ae_tmg(ae_initial, LACTIC_ACIDOSIS)

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(obj.final_ae_classification, self.get_ae_classification(HEPATOMEGALY))
        self.assertTrue(obj.verified)

    def test_rerunning_update_copies_on_a_verified_row_is_a_no_op(self):
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        self.backfill()
        ae_tmg.investigator_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_tmg.save()
        self.backfill(update_copies=True)
        obj = AeFinalClassification.objects.get()
        modified = obj.modified

        out = self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(obj.modified, modified)
        self.assertIn("skipped 1", out)

    # ------------------------------------------------------------------
    # a second AeTmg aborts the run (expected failure)
    # ------------------------------------------------------------------
    def test_second_ae_tmg_on_one_ae_initial_does_not_abort_the_run(self):
        """AeTmgAction is not a singleton, so two TMG reports are legal."""
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        self.get_ae_tmg(ae_initial, HEPATOMEGALY, original_report_agreed=NO)

        self.backfill()

        self.assertEqual(AeFinalClassification.objects.count(), 1)

    def test_second_ae_tmg_does_not_abort_a_dry_run(self):
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        self.get_ae_tmg(ae_initial, HEPATOMEGALY, original_report_agreed=NO)

        self.backfill(dry_run=True)

        self.assertEqual(AeFinalClassification.objects.count(), 0)
