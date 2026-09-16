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
* Resolving snapshots the source classifications into
  `resolved_ae_classification` and
  `resolved_investigator_ae_classification`, so the record says what
  the reviewer resolved against. The command never writes them.
* A frozen row is reported once its sources no longer match that
  snapshot, so a standing override stays quiet and re-resolving drains
  the row from the report.
* `Command.get_ae_tmg` suppresses only `DoesNotExist`, so a second
  AeTmg on the same AeInitial (allowed: `AeTmgAction` is not a
  singleton and lists itself as a parent action) aborts the whole run.
* `original_report_agreed` is where a TMG investigator says whether
  they agree with the classification on the original AE report: it is
  the question the AeTmg form asks, while
  `investigator_ae_classification_agreed` is not on that form and stays
  at its NOT_APPLICABLE default. Agreeing, they select no
  classification of their own, and the answer is the AeInitial's, taken
  from `ae_classification_other` where that classification is OTHER.
  Reading the absent selection as a disagreement puts an agreed record
  in front of a reviewer for nothing.
* Where there is more than one AeTmg they are weighed together: one
  investigator disagreeing is a disagreement whichever report came
  last, and the record requires review.
"""

from io import StringIO

from clinicedc_constants import GRADE4, NO, NOT_APPLICABLE, OTHER, PENDING, YES
from dateutil.relativedelta import relativedelta
from django.core.management import call_command
from django.test import TestCase, override_settings
from edc_adverse_event.models import AeClassification
from edc_utils import get_utcnow
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

    def get_ae_initial(
        self,
        classification_name: str = LACTIC_ACIDOSIS,
        ae_classification_other: str | None = None,
    ) -> AeInitial:
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        return baker.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=subject_consent.subject_identifier,
            ae_grade=GRADE4,
            ae_classification=self.get_ae_classification(classification_name),
            ae_classification_other=ae_classification_other,
        )

    def get_agreeing_ae_tmg(
        self,
        ae_initial: AeInitial,
        classification_name: str | None = None,
    ) -> AeTmg:
        """An AeTmg whose investigator agrees with the classification.

        There is nothing for them to select, so the classification is
        left null or sits at the NOT_APPLICABLE the form starts them on.
        """
        return baker.make_recipe(
            "meta_ae.aetmg",
            ae_initial=ae_initial,
            subject_identifier=ae_initial.subject_identifier,
            original_report_agreed=YES,
            investigator_ae_classification=(
                self.get_ae_classification(classification_name)
                if classification_name
                else None
            ),
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
        """Stand in for a reviewer settling the record on the form.

        A plain save, so the snapshot has to be taken by the model
        rather than by the form.
        """
        obj.final_ae_classification = self.get_ae_classification(classification_name)
        obj.conflict_resolved = YES
        obj.save()
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
    # an agreeing TMG selects no classification of its own
    # ------------------------------------------------------------------
    def test_a_tmg_agreeing_with_no_selection_agrees(self):
        """Nothing selected because there was nothing to correct."""
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        self.get_agreeing_ae_tmg(ae_initial)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, AGREED)
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )

    def test_a_tmg_agreeing_with_a_not_applicable_selection_agrees(self):
        """The same answer, spelled NOT_APPLICABLE rather than left null."""
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        self.get_agreeing_ae_tmg(ae_initial, NOT_APPLICABLE)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, AGREED)
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )

    def test_a_tmg_not_agreeing_and_selecting_nothing_requires_review(self):
        """Disagreement without a counter-proposal is still disagreement."""
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        baker.make_recipe(
            "meta_ae.aetmg",
            ae_initial=ae_initial,
            subject_identifier=ae_initial.subject_identifier,
            original_report_agreed=NO,
            investigator_ae_classification=self.get_ae_classification(NOT_APPLICABLE),
        )

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, REQUIRES_REVIEW)
        self.assertIsNone(obj.final_ae_classification)

    def test_an_agreeing_tmg_carries_an_other_classification_across(self):
        """Where the original says OTHER, the text is the answer."""
        ae_initial = self.get_ae_initial(OTHER, ae_classification_other="Pancreatitis")
        self.get_agreeing_ae_tmg(ae_initial)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, AGREED)
        self.assertEqual(obj.final_ae_classification, self.get_ae_classification(OTHER))
        self.assertEqual(obj.final_ae_classification_other, "Pancreatitis")

    def test_an_agreeing_tmg_resolves_an_other_naming_a_known_classification(self):
        """`other` text naming a classification on the list resolves to it."""
        ae_initial = self.get_ae_initial(OTHER, ae_classification_other="Lactic acidosis")
        self.get_agreeing_ae_tmg(ae_initial)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, AGREED)
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )

    def test_the_copied_agreement_reports_the_agreement(self):
        """`investigator_ae_classification_agreed` on the record.

        Labelled "TMG investigator agrees with the AE classification
        from the original AE report?", so it says whether they did,
        across every report.
        """
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        self.get_agreeing_ae_tmg(ae_initial, NOT_APPLICABLE)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.investigator_ae_classification_agreed, YES)

    def test_a_tmg_disagreeing_on_the_classification_requires_review(self):
        """The selection is only made where there is a disagreement."""
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        baker.make_recipe(
            "meta_ae.aetmg",
            ae_initial=ae_initial,
            subject_identifier=ae_initial.subject_identifier,
            original_report_agreed=NO,
            investigator_ae_classification=self.get_ae_classification(HEPATOMEGALY),
        )

        self.backfill()

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
    # resolving records what the reviewer resolved against
    # ------------------------------------------------------------------
    def test_resolving_snapshots_the_source_classifications(self):
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        self.backfill()

        obj = self.resolve(AeFinalClassification.objects.get(), HEPATOMEGALY)

        obj.refresh_from_db()
        self.assertEqual(
            obj.resolved_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )
        self.assertEqual(
            obj.resolved_investigator_ae_classification,
            self.get_ae_classification(LACTIC_ACIDOSIS),
        )

    def test_resolving_before_the_tmg_arrives_snapshots_a_null_tmg_side(self):
        self.get_ae_initial()
        self.backfill()

        obj = self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)

        obj.refresh_from_db()
        self.assertEqual(
            obj.resolved_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )
        self.assertIsNone(obj.resolved_investigator_ae_classification)

    def test_unresolving_clears_the_snapshot(self):
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        self.backfill()
        obj = self.resolve(AeFinalClassification.objects.get(), HEPATOMEGALY)

        obj.conflict_resolved = NO
        obj.save()

        obj.refresh_from_db()
        self.assertIsNone(obj.resolved_ae_classification)
        self.assertIsNone(obj.resolved_investigator_ae_classification)

    def test_command_never_writes_the_resolved_snapshot(self):
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        self.backfill()
        self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)

        ae_tmg.investigator_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_tmg.original_report_agreed = NO
        ae_tmg.save()

        self.backfill(update_copies=True)

        obj = AeFinalClassification.objects.get()
        self.assertEqual(
            obj.resolved_investigator_ae_classification,
            self.get_ae_classification(LACTIC_ACIDOSIS),
        )
        self.assertEqual(
            obj.investigator_ae_classification, self.get_ae_classification(HEPATOMEGALY)
        )

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

    def test_update_copies_reports_nothing_for_an_override_while_the_sources_hold(self):
        """A standing override is settled, not a discrepancy.

        The reviewer resolved against these very values, so nothing has
        happened since that they need to see.
        """
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        self.backfill()
        self.resolve(AeFinalClassification.objects.get(), HEPATOMEGALY)

        out = self.backfill(update_copies=True)

        self.assertNotIn("resolved, not changed", out)
        self.assertIn("Left 0 resolved row(s) unchanged.", out)

    def test_update_copies_reports_an_override_once_the_sources_move(self):
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        self.backfill()
        self.resolve(AeFinalClassification.objects.get(), HEPATOMEGALY)

        ae_tmg.investigator_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_tmg.original_report_agreed = NO
        ae_tmg.save()

        out = self.backfill(update_copies=True)

        self.assertIn(
            self.expected_discrepancy_line(
                ae_initial,
                final=HEPATOMEGALY,
                review_status=REQUIRES_REVIEW,
                sources=f"{LACTIC_ACIDOSIS}, {HEPATOMEGALY}",
            ),
            out,
        )
        self.assertIn("Left 1 resolved row(s) unchanged.", out)

    def test_update_copies_reports_a_row_resolved_before_its_tmg_arrived(self):
        """The reviewer resolved with no TMG input; now there is some."""
        ae_initial = self.get_ae_initial()
        self.backfill()
        self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)
        self.get_ae_tmg(ae_initial, HEPATOMEGALY, original_report_agreed=NO)

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

    def test_re_resolving_drains_the_row_from_the_report(self):
        """Re-snapshotting settles the row again."""
        ae_initial = self.get_ae_initial()
        ae_tmg = self.get_ae_tmg(ae_initial)
        self.backfill()
        self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)
        ae_tmg.investigator_ae_classification = self.get_ae_classification(HEPATOMEGALY)
        ae_tmg.original_report_agreed = NO
        ae_tmg.save()
        self.backfill(update_copies=True)

        self.resolve(AeFinalClassification.objects.get(), LACTIC_ACIDOSIS)
        out = self.backfill(update_copies=True)

        self.assertNotIn("resolved, not changed", out)
        self.assertIn("Left 0 resolved row(s) unchanged.", out)

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

    def make_ae_tmg(
        self,
        ae_initial: AeInitial,
        days_ago: int,
        agreed: str,
        classification_name: str | None = None,
    ) -> AeTmg:
        return baker.make_recipe(
            "meta_ae.aetmg",
            ae_initial=ae_initial,
            subject_identifier=ae_initial.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=days_ago),
            original_report_agreed=agreed,
            investigator_ae_classification=(
                self.get_ae_classification(classification_name)
                if classification_name
                else None
            ),
        )

    def test_every_ae_tmg_agreeing_agrees(self):
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        self.make_ae_tmg(ae_initial, days_ago=2, agreed=YES)
        self.make_ae_tmg(ae_initial, days_ago=1, agreed=YES)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, AGREED)
        self.assertEqual(
            obj.final_ae_classification, self.get_ae_classification(LACTIC_ACIDOSIS)
        )
        self.assertEqual(obj.investigator_ae_classification_agreed, YES)

    def test_one_ae_tmg_disagreeing_requires_review(self):
        """A later agreement does not overturn an earlier disagreement.

        Two investigators who do not say the same thing are a
        disagreement, whichever of them reported last.
        """
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        self.make_ae_tmg(ae_initial, days_ago=2, agreed=NO, classification_name=HEPATOMEGALY)
        self.make_ae_tmg(ae_initial, days_ago=1, agreed=YES)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, REQUIRES_REVIEW)
        self.assertIsNone(obj.final_ae_classification)
        self.assertEqual(obj.investigator_ae_classification_agreed, NO)

    def test_a_late_ae_tmg_disagreeing_requires_review(self):
        """The same two reports the other way round."""
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        self.make_ae_tmg(ae_initial, days_ago=2, agreed=YES)
        self.make_ae_tmg(ae_initial, days_ago=1, agreed=NO, classification_name=HEPATOMEGALY)

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.review_status, REQUIRES_REVIEW)
        self.assertIsNone(obj.final_ae_classification)
        self.assertEqual(obj.investigator_ae_classification_agreed, NO)

    def test_the_tmg_columns_show_the_latest_ae_tmg(self):
        """The record holds one of each, so they show the latest.

        The agreement is the exception: it is weighed across them all.
        """
        ae_initial = self.get_ae_initial(LACTIC_ACIDOSIS)
        self.make_ae_tmg(ae_initial, days_ago=2, agreed=YES)
        latest = self.make_ae_tmg(
            ae_initial, days_ago=1, agreed=NO, classification_name=HEPATOMEGALY
        )

        self.backfill()

        obj = AeFinalClassification.objects.get()
        self.assertEqual(obj.ae_tmg, latest)
        self.assertEqual(obj.ae_tmg_action_identifier, latest.action_identifier)
        self.assertEqual(
            obj.investigator_ae_classification, self.get_ae_classification(HEPATOMEGALY)
        )

    def test_second_ae_tmg_does_not_abort_a_dry_run(self):
        ae_initial = self.get_ae_initial()
        self.get_ae_tmg(ae_initial)
        self.get_ae_tmg(ae_initial, HEPATOMEGALY, original_report_agreed=NO)

        self.backfill(dry_run=True)

        self.assertEqual(AeFinalClassification.objects.count(), 0)
