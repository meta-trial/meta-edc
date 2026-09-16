"""Backfill AeFinalClassification rows from their source reports.

The work itself is in `meta_ae.backfill`, which the "Refresh from the
source reports" admin action also calls. This command is the
command-line face of it: it chooses the records, then says what came
back.

Idempotent: re-running only creates rows for AeInitials that don't
already have one. With ``--update-copies`` existing rows are refreshed
from the sources, including ``review_status`` and, where the reviewer
has not settled the record, ``final_ae_classification``. A record they
have settled keeps its classification whatever the sources say, and is
reported where the sources have moved since.

Usage::

    uv run manage.py backfill_ae_final_classification [--dry-run] [--update-copies]
"""

from django.core.management.base import BaseCommand

from meta_ae.backfill import BackfillResult, backfill_ae_final_classifications
from meta_ae.models import AeInitial


class Command(BaseCommand):
    help = (
        "Create AeFinalClassification rows from AeInitial (with optional "
        "linked AeTmg). Auto-fills final_ae_classification only when every "
        "AE TMG report agrees with the original AE report."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would be created/updated without changing the database.",
        )
        parser.add_argument(
            "--update-copies",
            action="store_true",
            help=(
                "Also refresh copied columns, review_status and, where the "
                "reviewer has not settled the record, final_ae_classification "
                "on existing AeFinalClassification rows."
            ),
        )

    def handle(self, *args, dry_run: bool = False, update_copies: bool = False, **options):  # noqa: ARG002
        qs = AeInitial.objects.all()
        self.stdout.write(f"Scanning {qs.count()} AeInitial row(s)...")
        result = backfill_ae_final_classifications(
            qs, dry_run=dry_run, update_copies=update_copies
        )
        self.report(result, dry_run=dry_run, update_copies=update_copies)

    def report(self, result: BackfillResult, dry_run: bool, update_copies: bool) -> None:
        for record in result.created:
            self.stdout.write(self.created_line(record, dry_run))
        for discrepancy in result.discrepancies:
            self.stdout.write(
                f"  ! resolved, not changed: "
                f"subject {discrepancy.subject_identifier} "
                f"ae_initial={discrepancy.ae_initial_action_identifier} "
                f"final={discrepancy.final} "
                f"review_status={discrepancy.review_status} "
                f"sources=({', '.join(discrepancy.sources)})"
            )
        verb = "would update" if dry_run else "updated"
        for record in result.updated:
            self.stdout.write(
                f"  ~ {verb} {', '.join(record.fields)} on "
                f"AeFinalClassification for subject {record.subject_identifier}"
            )

        verb_c = "Would create" if dry_run else "Created"
        verb_u = "Would update" if dry_run else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{verb_c} {len(result.created)}, {verb_u} {len(result.updated)}, "
                f"skipped {result.skipped} already-current."
            )
        )
        if update_copies:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Left {len(result.discrepancies)} resolved row(s) unchanged."
                )
            )

    @staticmethod
    def created_line(record, dry_run: bool) -> str:
        if not dry_run:
            return f"  + created AeFinalClassification for subject {record.subject_identifier}"
        tmg_desc = (
            f"ae_tmg={', '.join(record.ae_tmg_action_identifiers)}"
            if record.ae_tmg_action_identifiers
            else "no ae_tmg"
        )
        return (
            f"  + would create AeFinalClassification for subject "
            f"{record.subject_identifier} "
            f"(ae_initial={record.ae_initial_action_identifier}, {tmg_desc})"
        )
