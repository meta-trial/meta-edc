from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from clinicedc_constants import NOT_APPLICABLE, NULL_STRING, OTHER, YES
from django.apps import apps as django_apps
from tqdm import tqdm

from ..list_data import list_data

if TYPE_CHECKING:
    from django.apps.registry import Apps

__all__ = ["ConversionResult", "update_aeclassification_other_fields", "write_report"]

AE_CLASSIFICATION = "edc_adverse_event.aeclassification"

ALIASES = {
    "dyslipidemia": "dyslipidaemia",
    "dsylipidemia": "dyslipidaemia",
    "dysilipidemia": "dyslipidaemia",
    "dysipidemia": "dyslipidaemia",
    "dyslipaedemia": "dyslipidaemia",
    "anemia": "anaemia",
    "renal insufficiency": "renal_insufficiency",
    "renal insufficency": "renal_insufficiency",
    "renal insuficiency": "renal_insufficiency",
    "renal insuffeciency": "renal_insufficiency",
    "renal insuffiency": "renal_insufficiency",
    "death": "death",
    "hyperlipidemia": "hyperlipidaemia",
    "hyperamylasemia": "hyperamylasaemia",
    "hyper amylasaemia": "hyperamylasaemia",
    "hypercholesteremia": "hypercholesterolaemia",
    "hypercholesterolemia": "hypercholesterolaemia",
    "hyperuricemia": "hyperuricaemia",
    "hypertriglyceridemia": "hypertriglyceridaemia",
    "hypoalbuminemia": "hypoalbuminaemia",
    "liver insufficiency": "liver_insufficiency",
    "liver insufficency": "liver_insufficiency",
    "leucopenia": "leukopenia",
}


@dataclass
class ConversionResult:
    """What a conversion did, for the caller to report as it sees fit.

    `unmapped` and `ambiguous` are keyed by (model_name, the original
    free text) and counted, so the same text on twenty records is one
    line to read rather than twenty.
    """

    converted: int = 0
    repointed: int = 0
    unmapped: dict[tuple[str, str], int] = field(default_factory=dict)
    ambiguous: dict[tuple[str, str], int] = field(default_factory=dict)

    @property
    def left_as_other(self) -> int:
        return sum(self.unmapped.values()) + sum(self.ambiguous.values())


def normalized(value: str | None) -> str:
    """Casefold, collapse whitespace, treat `_` as a space."""
    return " ".join((value or "").replace("_", " ").split()).casefold()


def get_terms(
    list_model: str = AE_CLASSIFICATION,
    aliases: dict[str, str] | None = None,
) -> list[tuple[str, str]]:
    """Every term worth looking for, longest first, as (term, name).

    Both the name and the display_name are terms, so `lactic_acidosis`
    and "Lactic acidosis" each match. Longest first so a term that
    contains another wins: "hepatomegaly with steatosis" is matched
    before "hepatomegaly" can claim it.
    """
    names = [name for name, _ in list_data[list_model]]
    terms: set[tuple[str, str]] = set()
    for name, display_name in list_data[list_model]:
        if name in [OTHER, NOT_APPLICABLE]:
            continue
        terms |= {(normalized(name), name), (normalized(display_name), name)}
    for term, name in (aliases or {}).items():
        if name not in names:
            raise ValueError(f"Alias points at a name not on the list. Got {name}.")
        terms.add((normalized(term), name))
    return sorted((t for t in terms if t[0]), key=lambda t: len(t[0]), reverse=True)


def match_names(terms: list[tuple[str, str]], value: str | None) -> list[str]:
    text = normalized(value)
    if not text:
        return []
    names = []
    for term, name in terms:
        if name not in names and re.search(rf"\b{re.escape(term)}\b", text):
            names.append(name)
    return names


def check_names_exist(
    terms: list[tuple[str, str]],
    apps: Apps | None = None,
    using: str | None = None,
) -> None:
    """Fail before writing anything if a target name is not on the list."""
    ae_classification_model_cls = apps.get_model("edc_adverse_event", "AeClassification")
    wanted = {name for _, name in terms}
    found = set(
        ae_classification_model_cls.objects.using(using)
        .filter(name__in=wanted)
        .values_list("name", flat=True)
    )
    if missing := wanted - found:
        raise ValueError(
            f"Cannot convert. AeClassification rows do not exist for "
            f"{sorted(missing)}. Has meta_ae.list_data changed?"
        )


def repoint_resolved_snapshot(
    model_name: str,
    obj,
    ae_classification_obj,
    apps: Apps | None = None,
    using: str | None = None,
) -> int:
    """Keep a settled AeFinalClassification settled.

    `resolved_ae_classification` and
    `resolved_investigator_ae_classification` record what a reviewer
    resolved against. Converting a source from OTHER moves it out from
    under them, so every settled record would be reported as needing
    another look on the next --update-copies, over a change that carries
    no new clinical information.

    Only a snapshot still pointing at OTHER is moved, so a record that
    was already stale for some other reason stays stale.
    """
    afc_model_cls = apps.get_model("meta_ae", "AeFinalClassification")
    if model_name == "AeInitial":
        opts = dict(
            filter_kwargs={"ae_initial": obj, "resolved_ae_classification__name": OTHER},
            update_kwargs={"resolved_ae_classification": ae_classification_obj},
        )
    elif model_name == "AeTmg":
        opts = dict(
            filter_kwargs={
                "ae_tmg": obj,
                "resolved_investigator_ae_classification__name": OTHER,
            },
            update_kwargs={"resolved_investigator_ae_classification": ae_classification_obj},
        )
    else:
        raise ValueError(f"Invalid or unhandled model name. Got {model_name}.")
    return (
        afc_model_cls.objects.using(using)
        .filter(conflict_resolved=YES, **opts["filter_kwargs"])
        .update(**opts["update_kwargs"])
    )


def update_aeclassification_other_fields(
    aliases: dict[str, str] | None = None,
    apps: Apps | None = None,
    using: str | None = None,
    verbose: bool | None = None,
) -> ConversionResult:
    apps = apps or django_apps
    if aliases is None:
        aliases = ALIASES
    terms = get_terms(aliases=aliases)  # validates once, fails loudly
    check_names_exist(terms, apps=apps, using=using)
    ae_classification_model_cls = apps.get_model("edc_adverse_event", "AeClassification")
    opts = [
        ("AeInitial", "ae_classification"),
        ("HistoricalAeInitial", "ae_classification"),
        ("AeTmg", "investigator_ae_classification"),
        ("HistoricalAeTmg", "investigator_ae_classification"),
    ]
    unmapped = defaultdict(int)
    ambiguous = defaultdict(int)
    converted = 0
    repointed = 0
    for model_name, fld in opts:
        if verbose:
            tqdm.write(f"{model_name}")
        model_cls = apps.get_model("meta_ae", model_name)
        qs = model_cls.objects.using(using).filter(**{f"{fld}__name": OTHER})
        total = qs.count()
        for obj in tqdm(qs, total=total, disable=not verbose):
            other_value = getattr(obj, f"{fld}_other")
            names = match_names(terms, other_value)
            if len(names) != 1:
                # nothing recognised, or more than one condition named in
                # the one field. Either way it is not ours to decide, so
                # it stays OTHER and is reported.
                report = ambiguous if names else unmapped
                report[(model_name, (other_value or "").strip())] += 1
                continue
            ae_classification_obj = ae_classification_model_cls.objects.using(using).get(
                name=names[0]
            )
            # keep the free text, appending where a comment is already there
            new_comment = "; ".join(
                [v for v in [getattr(obj, f"{fld}_comment", ""), other_value] if v]
            )
            setattr(obj, fld, ae_classification_obj)
            setattr(obj, f"{fld}_other", NULL_STRING)
            setattr(obj, f"{fld}_comment", new_comment)
            obj.save_base(update_fields=[fld, f"{fld}_other", f"{fld}_comment"], using=using)
            converted += 1
            if model_name in ["AeInitial", "AeTmg"]:
                repointed += repoint_resolved_snapshot(
                    model_name, obj, ae_classification_obj, apps=apps, using=using
                )

    result = ConversionResult(
        converted=converted,
        repointed=repointed,
        unmapped=dict(unmapped),
        ambiguous=dict(ambiguous),
    )
    if verbose:
        write_report(result)
    return result


def write_report(result: ConversionResult) -> None:
    """Say what a conversion did, on stdout."""
    sys.stdout.write(f"Converted {result.converted} row(s) from {OTHER}.\n")
    sys.stdout.write(
        f"Re-pointed {result.repointed} resolved AeFinalClassification snapshot(s), "
        f"so settled records stay settled.\n"
    )
    for (model_name, value), count in sorted(result.unmapped.items()):
        sys.stdout.write(
            f"  ! left as OTHER, nothing recognised: {model_name} {value!r} ({count})\n"
        )
    for (model_name, value), count in sorted(result.ambiguous.items()):
        sys.stdout.write(
            f"  ! left as OTHER, names more than one: {model_name} {value!r} ({count})\n"
        )
