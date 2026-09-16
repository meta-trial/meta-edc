"""Backfill AeFinalClassification rows from their source reports.

AeInitial is the starting document; an AeTmg is a child action of
AeInitial that may or may not exist yet. For each ``AeInitial`` this
command ensures a skeleton ``AeFinalClassification`` exists with the
read-only columns pre-filled from the sources. If the matching
``AeTmg`` is absent, the TMG-side copy columns are left null and
``review_status`` stays ``PENDING``.

``final_ae_classification`` is autofilled only when both source
classifications are set, agree, and neither is ``OTHER``, which is the
``AGREED`` review status. Where they do not agree the answer is a
reviewer's to give and the row is left ``REQUIRES_REVIEW``.

Idempotent: re-running only creates rows for AeInitials that don't
already have one. With ``--update-copies`` existing rows are refreshed
from the sources, including ``review_status`` and, where the reviewer
has not settled the record, ``final_ae_classification``.

A record the reviewer has settled (``conflict_resolved`` is ``YES``)
keeps its ``final_ae_classification`` whatever the sources say. Where
the sources have moved since they settled it, the row is reported
rather than changed, so the discrepancy is visible to a human.

Usage::

    uv run manage.py backfill_ae_final_classification [--dry-run] [--update-copies]
"""

import contextlib

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from meta_ae.models import AeFinalClassification, AeInitial, AeTmg
from meta_ae.models.ae_final_classification import (
    get_ae_values_to_copy,
    get_final_ae_classification,
    get_refresh_values,
    refresh_copies_from_sources,
    resolution_is_stale,
)


class Command(BaseCommand):
    help = (
        "Create AeFinalClassification rows from AeInitial (with optional "
        "linked AeTmg). Auto-fills final_ae_classification only when both "
        "sources agree and neither is OTHER."
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
        created = 0
        updated = 0
        skipped = 0
        unchanged_resolved = 0

        qs = AeInitial.objects.all().order_by("created")
        total = qs.count()
        self.stdout.write(f"Scanning {total} AeInitial row(s)...")

        for ae_initial_obj in qs.iterator():
            ae_final_obj = self.get_ae_final_classification(ae_initial_obj)
            aetmg_obj = self.get_ae_tmg(ae_initial_obj)

            if not ae_final_obj:
                created += 1
                self.create_ae_final_classification(ae_initial_obj, aetmg_obj, dry_run)
                continue

            if not update_copies:
                skipped += 1
                continue

            if resolution_is_stale(ae_final_obj, ae_initial_obj, aetmg_obj):
                unchanged_resolved += 1
                self.report_discrepancy(ae_final_obj, ae_initial_obj, aetmg_obj)

            if dry_run:
                values = get_refresh_values(ae_final_obj, ae_initial_obj, aetmg_obj)
                diffs = sorted(f for f, v in values.items() if getattr(ae_final_obj, f) != v)
                if not diffs:
                    skipped += 1
                    continue
                self.stdout.write(
                    f"  ~ would update {', '.join(diffs)} on "
                    f"AeFinalClassification for subject "
                    f"{ae_initial_obj.subject_identifier}"
                )
                updated += 1
                continue

            changed = refresh_copies_from_sources(ae_final_obj, ae_initial_obj, aetmg_obj)
            if not changed:
                skipped += 1
                continue
            updated += 1
            self.stdout.write(
                f"  ~ updated {', '.join(sorted(changed))} on "
                f"AeFinalClassification for subject {ae_initial_obj.subject_identifier}"
            )

        verb_c = "Would create" if dry_run else "Created"
        verb_u = "Would update" if dry_run else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{verb_c} {created}, {verb_u} {updated}, skipped {skipped} already-current."
            )
        )
        if update_copies:
            self.stdout.write(
                self.style.SUCCESS(f"Left {unchanged_resolved} resolved row(s) unchanged.")
            )

    def create_ae_final_classification(
        self, ae_initial_obj: AeInitial, aetmg_obj: AeTmg | None, dry_run: bool
    ) -> None:
        copy_values = get_ae_values_to_copy(ae_initial_obj, aetmg_obj)
        (
            copy_values["final_ae_classification"],
            copy_values["final_ae_classification_other"],
            copy_values["review_status"],
        ) = get_final_ae_classification(ae_initial_obj, aetmg_obj)
        if dry_run:
            tmg_desc = (
                f"ae_tmg={aetmg_obj.action_identifier}"
                if aetmg_obj is not None
                else "no ae_tmg"
            )
            self.stdout.write(
                f"  + would create AeFinalClassification for subject "
                f"{ae_initial_obj.subject_identifier} "
                f"(ae_initial={ae_initial_obj.action_identifier}, {tmg_desc})"
            )
            return
        with transaction.atomic():
            AeFinalClassification.objects.create(
                subject_identifier=ae_initial_obj.subject_identifier,
                site_id=ae_initial_obj.site_id,
                report_datetime=timezone.now(),
                user_created="django",
                **copy_values,
            )
        self.stdout.write(
            f"  + created AeFinalClassification for subject "
            f"{ae_initial_obj.subject_identifier}"
        )

    def report_discrepancy(
        self,
        ae_final_obj: AeFinalClassification,
        ae_initial_obj: AeInitial,
        aetmg_obj: AeTmg | None,
    ) -> None:
        """Say what the record holds and what the sources now say."""
        _, _, review_status = get_final_ae_classification(ae_initial_obj, aetmg_obj)
        sources = ", ".join(
            [
                self.classification_name(ae_initial_obj.ae_classification),
                self.classification_name(
                    aetmg_obj.investigator_ae_classification if aetmg_obj else None
                ),
            ]
        )
        self.stdout.write(
            f"  ! resolved, not changed: subject {ae_initial_obj.subject_identifier} "
            f"ae_initial={ae_initial_obj.action_identifier} "
            f"final={self.classification_name(ae_final_obj.final_ae_classification)} "
            f"review_status={review_status} sources=({sources})"
        )

    @staticmethod
    def classification_name(obj) -> str:
        return obj.name if obj is not None else "None"

    @staticmethod
    def get_ae_tmg(ae_initial: AeInitial) -> AeTmg | None:
        """Return the most recent AeTmg child-action of this AeInitial.

        AeTmg is linked to AeInitial via its action_identifier
        (AeInitial is the parent action). More than one is legal:
        AeTmgAction is not a singleton and names itself among its own
        parent actions, so take the latest rather than raising.
        """
        return AeTmg.objects.filter(ae_initial=ae_initial).order_by("report_datetime").last()

    @staticmethod
    def get_ae_final_classification(ae_initial: AeInitial) -> AeFinalClassification | None:
        """Return the AEFinalClassification instance or None."""
        obj = None
        with contextlib.suppress(AeFinalClassification.DoesNotExist):
            obj = AeFinalClassification.objects.get(ae_initial=ae_initial)
        return obj
