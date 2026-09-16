"""Build AeFinalClassification records from their source reports.

AeInitial is the starting document; an AeTmg is a child action of
AeInitial that may or may not exist yet. For each AeInitial this
ensures an AeFinalClassification exists with the read-only columns
pre-filled from the sources.

The work is here rather than in the management command so an admin
action can do the same thing to a handful of records that the command
does to all of them. Nothing here prints: `backfill_ae_final_
classifications` returns a `BackfillResult` and leaves each caller to
say it in its own voice.
"""

from dataclasses import dataclass, field

from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from .models import AeFinalClassification, AeInitial, AeTmg
from .models.ae_final_classification import (
    get_ae_values_to_copy,
    get_final_ae_classification,
    get_latest_ae_tmg,
    get_refresh_values,
    refresh_copies_from_sources,
    resolution_is_stale,
)


@dataclass
class CreatedRecord:
    subject_identifier: str
    ae_initial_action_identifier: str
    ae_tmg_action_identifiers: list[str] = field(default_factory=list)


@dataclass
class UpdatedRecord:
    subject_identifier: str
    fields: list[str] = field(default_factory=list)


@dataclass
class Discrepancy:
    """A settled record the sources have moved away from.

    The reviewer resolved against values that have since changed, so
    this says what the record holds and what the sources now say. It is
    not acted on: `conflict_resolved` is theirs, not ours.
    """

    subject_identifier: str
    ae_initial_action_identifier: str
    final: str
    review_status: str
    sources: tuple[str, str]


@dataclass
class BackfillResult:
    total: int = 0
    skipped: int = 0
    created: list[CreatedRecord] = field(default_factory=list)
    updated: list[UpdatedRecord] = field(default_factory=list)
    discrepancies: list[Discrepancy] = field(default_factory=list)


def get_ae_tmgs(ae_initial: AeInitial) -> list[AeTmg]:
    """Every AeTmg child-action of this AeInitial, oldest first.

    AeTmg is linked to AeInitial via its action_identifier (AeInitial
    is the parent action). More than one is legal: AeTmgAction is not a
    singleton and names itself among its own parent actions. They are
    weighed together, so one investigator disagreeing is a disagreement
    whichever report came last. `created` breaks a tie on
    report_datetime so the columns that show the latest cannot change
    between reruns.
    """
    return list(
        AeTmg.objects.filter(ae_initial=ae_initial).order_by("report_datetime", "created")
    )


def get_ae_final_classification(ae_initial: AeInitial) -> AeFinalClassification | None:
    return AeFinalClassification.objects.filter(ae_initial=ae_initial).first()


def classification_name(obj) -> str:
    return obj.name if obj is not None else "None"


def get_discrepancy(
    ae_final_obj: AeFinalClassification,
    ae_initial_obj: AeInitial,
    aetmg_objs: list[AeTmg],
) -> Discrepancy:
    _, _, review_status = get_final_ae_classification(ae_initial_obj, aetmg_objs)
    aetmg_obj = get_latest_ae_tmg(aetmg_objs)
    return Discrepancy(
        subject_identifier=ae_initial_obj.subject_identifier,
        ae_initial_action_identifier=ae_initial_obj.action_identifier,
        final=classification_name(ae_final_obj.final_ae_classification),
        review_status=review_status,
        sources=(
            classification_name(ae_initial_obj.ae_classification),
            classification_name(
                aetmg_obj.investigator_ae_classification if aetmg_obj else None
            ),
        ),
    )


def create_ae_final_classification(
    ae_initial_obj: AeInitial, aetmg_objs: list[AeTmg], dry_run: bool
) -> CreatedRecord:
    copy_values = get_ae_values_to_copy(ae_initial_obj, aetmg_objs)
    (
        copy_values["final_ae_classification"],
        copy_values["final_ae_classification_other"],
        copy_values["review_status"],
    ) = get_final_ae_classification(ae_initial_obj, aetmg_objs)
    if not dry_run:
        with transaction.atomic():
            AeFinalClassification.objects.create(
                subject_identifier=ae_initial_obj.subject_identifier,
                site_id=ae_initial_obj.site_id,
                report_datetime=timezone.now(),
                user_created="django",
                **copy_values,
            )
    return CreatedRecord(
        subject_identifier=ae_initial_obj.subject_identifier,
        ae_initial_action_identifier=ae_initial_obj.action_identifier,
        ae_tmg_action_identifiers=[obj.action_identifier for obj in aetmg_objs],
    )


def get_pending_updates(
    ae_final_obj: AeFinalClassification,
    ae_initial_obj: AeInitial,
    aetmg_objs: list[AeTmg],
) -> list[str]:
    """Fields a refresh would write, without writing them."""
    values = get_refresh_values(ae_final_obj, ae_initial_obj, aetmg_objs)
    return sorted(f for f, v in values.items() if getattr(ae_final_obj, f) != v)


def backfill_ae_final_classifications(
    qs: QuerySet[AeInitial],
    dry_run: bool = False,
    update_copies: bool = False,
) -> BackfillResult:
    """Create or refresh an AeFinalClassification per AeInitial in `qs`.

    Without `update_copies` an AeInitial that already has a record is
    left alone. With it, the copied columns and `review_status` refresh,
    and so does `final_ae_classification` where the reviewer has not
    settled the record. Records they have settled are reported instead
    of changed, where the sources have moved since.
    """
    result = BackfillResult(total=qs.count())

    for ae_initial_obj in qs.order_by("created").iterator():
        ae_final_obj = get_ae_final_classification(ae_initial_obj)
        aetmg_objs = get_ae_tmgs(ae_initial_obj)

        if not ae_final_obj:
            result.created.append(
                create_ae_final_classification(ae_initial_obj, aetmg_objs, dry_run)
            )
            continue

        if not update_copies:
            result.skipped += 1
            continue

        if resolution_is_stale(ae_final_obj, ae_initial_obj, aetmg_objs):
            result.discrepancies.append(
                get_discrepancy(ae_final_obj, ae_initial_obj, aetmg_objs)
            )

        if dry_run:
            changed = get_pending_updates(ae_final_obj, ae_initial_obj, aetmg_objs)
        else:
            changed = sorted(
                refresh_copies_from_sources(ae_final_obj, ae_initial_obj, aetmg_objs)
            )
        if not changed:
            result.skipped += 1
            continue
        result.updated.append(
            UpdatedRecord(subject_identifier=ae_initial_obj.subject_identifier, fields=changed)
        )

    return result
