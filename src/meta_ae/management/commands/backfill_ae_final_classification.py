"""Backfill AeFinalClassification rows from their source reports.

AeInitial is the starting document; an AeTmg is a child action of
AeInitial that may or may not exist yet. For each ``AeInitial`` this
command ensures a skeleton ``AeFinalClassification`` exists with the
read-only columns pre-filled from the sources. If the matching
``AeTmg`` is absent, the TMG-side copy columns are left null and
``final_ae_classification`` is not autofilled.

``final_ae_classification`` is autofilled only when both source
classifications are set, agree, and neither is ``OTHER``.

Idempotent: re-running only creates rows for AeInitials that don't
already have one. With ``--update-copies`` existing rows are
refreshed from the sources; if either ``ae_classification`` or
``investigator_ae_classification`` changes on refresh, the existing
``final_ae_classification`` is cleared so the investigator must
reassess.

Usage::

    uv run manage.py backfill_ae_final_classification [--dry-run] [--update-copies]
"""

import contextlib

from clinicedc_constants import NOT_APPLICABLE, NULL_STRING, OTHER, YES
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from edc_adverse_event.models import AeClassification

from meta_ae.models import AeFinalClassification, AeInitial, AeTmg
from meta_ae.models.ae_final_classification import (
    get_ae_values_to_copy,
    refresh_copies_from_sources,
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
                "Also refresh copied columns on existing AeFinalClassification "
                "rows. If ae_classification or investigator_ae_classification "
                "changes, final_ae_classification is cleared so the investigator "
                "must reassess."
            ),
        )

    def handle(self, *args, dry_run: bool = False, update_copies: bool = False, **options):  # noqa: ARG002
        created = 0
        updated = 0
        skipped = 0

        qs = AeInitial.objects.all().order_by("created")
        total = qs.count()
        self.stdout.write(f"Scanning {total} AeInitial row(s)...")

        for ae_initial_obj in qs.iterator():
            ae_final_obj = self.get_ae_final_classification(ae_initial_obj)
            aetmg_obj = self.get_ae_tmg(ae_initial_obj)

            if not ae_final_obj:
                copy_values = get_ae_values_to_copy(ae_initial_obj, aetmg_obj)
                (
                    copy_values["final_ae_classification"],
                    copy_values["final_ae_classification_other"],
                    copy_values["verified"],
                ) = self.get_final_ae_classification(ae_initial_obj, aetmg_obj)
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
                    created += 1
                    continue
                with transaction.atomic():
                    AeFinalClassification.objects.create(
                        subject_identifier=ae_initial_obj.subject_identifier,
                        site_id=ae_initial_obj.site_id,
                        report_datetime=timezone.now(),
                        user_created="django",
                        **copy_values,
                    )
                created += 1
                self.stdout.write(
                    f"  + created AeFinalClassification for subject "
                    f"{ae_initial_obj.subject_identifier}"
                )
                continue

            if not update_copies:
                skipped += 1
                continue

            if dry_run:
                new_values = get_ae_values_to_copy(ae_initial_obj, aetmg_obj)
                diffs = {f: v for f, v in new_values.items() if getattr(ae_final_obj, f) != v}
                if not diffs:
                    skipped += 1
                    continue
                if (
                    any(
                        f in diffs
                        for f in ("ae_classification", "investigator_ae_classification")
                    )
                    and ae_final_obj.final_ae_classification_id is not None
                ):
                    # Mirror the clear performed in refresh_copies_from_sources
                    # so the dry-run summary matches the real write path.
                    diffs["final_ae_classification"] = None
                    diffs["final_ae_classification_other"] = NULL_STRING
                    diffs["verified"] = False
                self.stdout.write(
                    f"  ~ would update {', '.join(sorted(diffs))} on "
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

    @staticmethod
    def get_ae_tmg(ae_initial: AeInitial) -> AeTmg | None:
        """Return the AeTmg child-action of this AeInitial, or None.

        AeTmg is linked to AeInitial via its action_identifier
        (AeInitial is the parent action).
        """
        obj = None
        with contextlib.suppress(AeTmg.DoesNotExist):
            obj = AeTmg.objects.get(ae_initial=ae_initial)
        return obj

    @staticmethod
    def get_ae_final_classification(ae_initial: AeInitial) -> AeFinalClassification | None:
        """Return the AEFinalClassification instance or None."""
        obj = None
        with contextlib.suppress(AeFinalClassification.DoesNotExist):
            obj = AeFinalClassification.objects.get(ae_initial=ae_initial)
        return obj

    @staticmethod
    def get_final_ae_classification(
        ae_initial_obj: AeInitial, aetmg_obj: AeTmg | None
    ) -> tuple[AeClassification | None, str | None, bool]:
        """Return an AeClassification instance only when both sides are
        present and agree. Disregard if either is OTHER.
        """
        ae_classification_obj: AeClassification | None = None
        ae_classification_other: str | None = None
        verified: bool = False
        if aetmg_obj:
            ae_classification_obj = ae_initial_obj.ae_classification
            tmg_classification_obj = aetmg_obj.investigator_ae_classification
            either_is_other = (
                ae_classification_obj is not None and ae_classification_obj.name == OTHER
            ) or (tmg_classification_obj is not None and tmg_classification_obj.name == OTHER)
            if (
                not either_is_other
                and ae_classification_obj is not None
                and tmg_classification_obj is not None
                and (
                    ae_classification_obj == tmg_classification_obj
                    or (
                        aetmg_obj.original_report_agreed == YES
                        and tmg_classification_obj.name == NOT_APPLICABLE
                    )
                )
            ):
                verified = True
            elif (
                aetmg_obj.original_report_agreed == YES
                and ae_classification_obj is not None
                and ae_classification_obj.name == OTHER
            ):
                try:
                    ae_classification_obj = AeClassification.objects.get(
                        Q(name=ae_initial_obj.ae_classification_other.lower())
                        | Q(display_name=ae_initial_obj.ae_classification_other)
                    )
                    verified = True
                except AeClassification.DoesNotExist:
                    ae_classification_other = ae_initial_obj.ae_classification_other
            else:
                ae_classification_obj = None
        return ae_classification_obj, ae_classification_other or NULL_STRING, verified
