"""Tests for the rerun behaviour of `backfill_ae_final_classification`.

These tests describe the target behaviour and are expected to fail
until the model and command are reworked. They cover four things:

* `review_status` is the command's own verdict on the sources:
  `PENDING` while no AeTmg exists, `AGREED` when the two
  classifications agree, `REQUIRES_REVIEW` when they do not. It is
  recomputed on every pass.
* `conflict_resolved` is the reviewer's tick, and the command never
  writes it. `conflict_resolved == YES` freezes
  `final_ae_classification` whatever the `review_status`, so a reviewer
  may also overrule an `AGREED` row; anything else leaves the row open
  to the command.
* Whenever the command would have written a different
  `final_ae_classification` but may not, it reports the row, so every
  discrepancy it cannot act on is visible to a human. That covers both
  a frozen row whose sources have moved and a reviewer overruling the
  sources.
* `Command.get_ae_tmg` suppresses only `DoesNotExist`, so a second
  AeTmg on the same AeInitial (allowed: `AeTmgAction` is not a
  singleton and lists itself as a parent action) aborts the whole run.
"""

from io import StringIO

from clinicedc_constants import GRADE4, NO, NOT_APPLICABLE, PENDING, YES
from django.core.management import call_command
from django.test import TestCase, override_settings
from edc_adverse_event.models import AeClassification
from model_bakery import baker
from multisite import SiteID

from meta_ae.models import AeFinalClassification, AeInitial, AeTmg
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin

# spelled out here rather than imported so a missing constants module
# does not stop the whole module from loading. These belong in
# meta_ae.constants alongside a choices tuple.
AGREED = "agreed"
REQUIRES_REVIEW = "requires_review"

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

    def resolve(
        self,
        obj: AeFinalClassification,
        classification_name: str = LACTIC_ACIDOSIS,
    ) -> AeFinalClassification:
        """Stand in for a reviewer settling the conflict on the form."""
        obj.final_ae_classification = self.get_ae_classification(classification_name)
        obj.conflict_resolved = YES
        obj.save(update_fields=["final_ae_classification", "conflict_resolved"])
        return obj

    @staticmethod
    def backfill(**kwargs) -> str:
        out = StringIO()
        call_command("backfill_ae_final_classification", stdout=out, **kwargs)
        return out.getvalue()

    # ------------------------------------------------------------------
    # rerunning with no flags is a no-op
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
    # review_status is the command's verdict on the sources
    # ------------------------------------------------------------------
    def test_create_path_is_pending_while_there_is_no_ae_tmg(self):
        self.get_ae_initial()

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, PENDING)
        self.assertIsNone(obj.final_ae_classification)

    def test_create_path_agrees_and_autofills_when_sources_agree(self):
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, AGREED)
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )

    def test_create_path_requires_review_when_sources_disagree(self):
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        self.get_ae_tmg(ae_initial, HEPATOMEGALY, original_report_agreed=NO)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, REQUIRES_REVIEW)
        self.assertIsNone(obj.final_ae_classification)

    def test_command_never_writes_conflict_resolved(self):
        """The reviewer owns the tick; the command only ever reads it."""
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        self.get_ae_tmg(ae_initial, HEPATOMEGALY, original_report_agreed=NO)
        self.backfill()
        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, REQUIRES_REVIEW)
        self.assertEqual(obj.conflict_resolved, NOT_APPLICABLE)

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(obj.conflict_resolved, NOT_APPLICABLE)

    def test_update_copies_recomputes_review_status_when_sources_diverge(self):
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        self.backfill()
        self.assertEqual(AeFinalClassification.objects.get().review_status, AGREED)

        ae_tmg.investigator_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_tmg.original_report_agreed = NO
        ae_tmg.save()

        self.backfill(update_copies=True)

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, REQUIRES_REVIEW)
        self.assertIsNone(obj.final_ae_classification)

    # ------------------------------------------------------------------
    # --update-copies picks up an AeTmg added since the last run
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

    def test_update_copies_autofills_final_classification_when_tmg_added_later(self):
        """A row backfilled before its AeTmg existed must catch up.

        Once refreshed it should be indistinguishable from a row
        backfilled after the AeTmg arrived.
        """
        ae_initial = self.get_ae_initial()
        self.backfill()
        self.get_ae_tmg(ae_initial)

        self.backfill(update_copies=True)

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, AGREED)
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )

    def test_update_copies_may_change_an_unresolved_final_classification(self):
        """An unresolved row is the command's to revise."""
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        self.backfill()
        obj = AeFinalClassification.objects.get()
        obj.final_ae_classification = self.get_ae_classification(LACTIC_ACIDOSIS)
        obj.save(update_fields=["final_ae_classification"])
        self.assertNotEqual(obj.conflict_resolved, YES)
        self.get_ae_tmg(ae_initial, HEPATOMEGALY, original_report_agreed=NO)

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(obj.review_status, REQUIRES_REVIEW)
        self.assertIsNone(obj.final_ae_classification)

    # ------------------------------------------------------------------
    # conflict_resolved == YES freezes final_ae_classification
    # ------------------------------------------------------------------
    def test_update_copies_leaves_a_resolved_final_classification_when_tmg_changes(self):
        """The copies still refresh; the reviewer's answer does not move."""
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        self.backfill()
        obj = self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)

        ae_tmg.investigator_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_tmg.original_report_agreed = NO
        ae_tmg.save()

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )
        self.assertEqual(obj.conflict_resolved, YES)
        self.assertEqual(
            obj.investigator_ae_classification, self.get_ae_classification(HEPATOMEGALY)
        )
        self.assertEqual(obj.investigator_ae_classification_agreed, NO)

    def test_update_copies_leaves_a_resolved_final_classification_when_ae_initial_changes(
        self,
    ):
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        self.backfill()
        obj = self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)

        ae_initial.ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_initial.save()

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )
        self.assertEqual(obj.conflict_resolved, YES)
        self.assertEqual(obj.ae_classification, self.get_ae_classification(HEPATOMEGALY))

    def test_update_copies_leaves_a_resolved_final_classification_when_tmg_added_later(
        self,
    ):
        """A row resolved before its AeTmg arrived keeps its answer."""
        ae_initial = self.get_ae_initial()
        self.backfill()
        obj = self.resolve(AeFinalClassification.objects.get(), HEPATOMEGALY)
        self.get_ae_tmg(ae_initial, LACTIC_ACIDOSIS)

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(obj.final_ae_classification, self.get_ae_classification(HEPATOMEGALY))
        self.assertEqual(obj.conflict_resolved, YES)

    def test_update_copies_leaves_a_reviewer_override_of_an_agreed_row(self):
        """The tick outranks the command's own verdict.

        The sources still agree, so `review_status` stays AGREED, but
        the answer is the reviewer's.
        """
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        self.backfill()
        obj = self.resolve(AeFinalClassification.objects.get(), HEPATOMEGALY)

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(obj.final_ae_classification, self.get_ae_classification(HEPATOMEGALY))
        self.assertEqual(obj.conflict_resolved, YES)
        self.assertEqual(obj.review_status, AGREED)

    def test_update_copies_sends_a_stale_resolved_row_back_for_review(self):
        """Frozen, but the sources moved, so the reviewer sees it again.

        `review_status` recomputes while `conflict_resolved` stays YES.
        That pair is the stale-resolution queue.
        """
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        self.backfill()
        obj = self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)
        self.assertEqual(obj.review_status, AGREED)

        ae_tmg.investigator_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_tmg.original_report_agreed = NO
        ae_tmg.save()

        self.backfill(update_copies=True)

        obj.refresh_from_db()
        self.assertEqual(obj.review_status, REQUIRES_REVIEW)
        self.assertEqual(obj.conflict_resolved, YES)

    def test_rerunning_update_copies_on_a_resolved_row_is_a_no_op(self):
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        self.backfill()
        self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)
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
    # discrepancies the command may not act on are reported
    # ------------------------------------------------------------------
    @staticmethod
    def expected_discrepancy_line(
        ae_initial: AeInitial,
        final: str,
        review_status: str,
        sources: str,
    ) -> str:
        """The row, what it holds, and what the sources now say."""
        return (
            f"  ! resolved, not changed: subject {ae_initial.subject_identifier} "
            f"ae_initial={ae_initial.action_identifier} final={final} "
            f"review_status={review_status} sources=({sources})"
        )

    def test_update_copies_reports_a_resolved_row_whose_sources_moved(self):
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        self.backfill()
        self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)

        ae_tmg.investigator_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_tmg.original_report_agreed = NO
        ae_tmg.save()

        out = self.backfill(update_copies=True)

        self.assertIn(
            self.expected_discrepancy_line(
                ae_initial,
                final=LACTIC_ACIDOSIS,
                review_status=REQUIRES_REVIEW,
                sources=f"{LACTIC_ACIDOSIS}, {HEPATOMEGALY}",
            ),
            out,
        )
        self.assertIn("Left 1 resolved row(s) unchanged.", out)

    def test_update_copies_reports_a_reviewer_override_of_an_agreed_row(self):
        """No source moved; the reviewer simply disagrees with the sources."""
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        self.backfill()
        self.resolve(AeFinalClassification.objects.get(), HEPATOMEGALY)

        out = self.backfill(update_copies=True)

        self.assertIn(
            self.expected_discrepancy_line(
                ae_initial,
                final=HEPATOMEGALY,
                review_status=AGREED,
                sources=f"{LACTIC_ACIDOSIS}, {LACTIC_ACIDOSIS}",
            ),
            out,
        )
        self.assertIn("Left 1 resolved row(s) unchanged.", out)

    def test_dry_run_update_copies_reports_a_resolved_row_it_may_not_change(self):
        """The report is obtainable without writing anything."""
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        self.backfill()
        self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)
        ae_tmg.investigator_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_tmg.original_report_agreed = NO
        ae_tmg.save()

        out = self.backfill(update_copies=True, dry_run=True)

        self.assertIn(
            self.expected_discrepancy_line(
                ae_initial,
                final=LACTIC_ACIDOSIS,
                review_status=REQUIRES_REVIEW,
                sources=f"{LACTIC_ACIDOSIS}, {HEPATOMEGALY}",
            ),
            out,
        )
        self.assertIn("Left 1 resolved row(s) unchanged.", out)
        obj = AeFinalClassification.objects.get()
        self.assertEqual(
            obj.investigator_ae_classification,
            self.get_ae_classification(LACTIC_ACIDOSIS),
        )

    def test_update_copies_reports_nothing_for_a_resolved_row_still_in_step(self):
        """Resolved to the same answer the sources give: no discrepancy."""
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        self.backfill()
        self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)

        out = self.backfill(update_copies=True)

        self.assertNotIn("resolved, not changed", out)
        self.assertIn("Left 0 resolved row(s) unchanged.", out)

    def test_update_copies_reports_nothing_for_an_unresolved_row(self):
        """An unresolved row is simply revised, so there is no discrepancy."""
        ae_initial = self.get_ae_initial()
        self.backfill()
        obj = AeFinalClassification.objects.get()
        obj.final_ae_classification = self.get_ae_classification(LACTIC_ACIDOSIS)
        obj.save(update_fields=["final_ae_classification"])
        self.get_ae_tmg(ae_initial, HEPATOMEGALY, original_report_agreed=NO)

        out = self.backfill(update_copies=True)

        self.assertNotIn("resolved, not changed", out)
        self.assertIn("Left 0 resolved row(s) unchanged.", out)

    # ------------------------------------------------------------------
    # a second AeTmg aborts the run
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
