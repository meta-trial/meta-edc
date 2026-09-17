from clinicedc_constants import NO, NOT_APPLICABLE, NULL_STRING, OTHER, PENDING, YES
from clinicedc_constants.choices import YES_NO, YES_NO_NA
from django.db import models
from django.db.models import Q
from django.utils import timezone
from edc_adverse_event.models import AeClassification
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model_fields.fields import OtherCharField
from edc_sites.managers import CurrentSiteManager
from edc_sites.model_mixins import SiteModelMixin

from ..choices import REVIEW_STATUS
from ..constants import AGREED, REQUIRES_REVIEW
from .ae_initial import AeInitial
from .ae_tmg import AeTmg

RESOLVED_SNAPSHOT_FIELDS = (
    "resolved_ae_classification",
    "resolved_investigator_ae_classification",
)


class ModelManager(models.Manager):
    use_in_migrations = True


def get_latest_ae_tmg(ae_tmgs: "list[AeTmg]") -> "AeTmg | None":
    """The TMG's current position, or None where there is no report."""
    return ae_tmgs[-1] if ae_tmgs else None


def ae_tmg_agrees(ae_initial: "AeInitial", ae_tmg: "AeTmg") -> bool:
    """True where this TMG report agrees with the original classification.

    `original_report_agreed` is the question the AeTmg form actually
    asks; `investigator_ae_classification_agreed` is not on the form and
    stays at its NOT_APPLICABLE default, so it says nothing. An
    investigator selects a classification of their own only where they
    disagree, so YES is the agreement itself, however the unused
    selection happens to be left. Where they did not answer, the two
    classifications have to match on their own.
    """
    if ae_tmg.original_report_agreed == YES:
        return True
    ae_classification_obj = ae_initial.ae_classification
    tmg_classification_obj = ae_tmg.investigator_ae_classification
    unusable = [OTHER, NOT_APPLICABLE]
    return (
        ae_classification_obj is not None
        and tmg_classification_obj is not None
        and ae_classification_obj.name not in unusable
        and tmg_classification_obj.name not in unusable
        and ae_classification_obj == tmg_classification_obj
    )


def get_investigator_ae_classification_agreed(
    ae_initial: "AeInitial", ae_tmgs: "list[AeTmg]"
) -> str:
    """Whether the TMG agrees with the original classification.

    Derived across every TMG report, not copied from one of them: one
    investigator disagreeing is a disagreement, whatever the others
    said and whichever came last. The answer on each report is
    `original_report_agreed`.
    """
    if not ae_tmgs:
        return NULL_STRING
    return YES if all(ae_tmg_agrees(ae_initial, obj) for obj in ae_tmgs) else NO


def get_ae_values_to_copy(ae_initial: "AeInitial", ae_tmgs: "list[AeTmg]") -> dict:
    """Values that AeFinalClassification copies from the source reports.

    `ae_tmgs` may be empty: an AeInitial may exist without any AeTmg.
    In that case only the AeInitial-side fields are returned, and the
    ae_tmg-side fields are nulled so a subsequent refresh clears any
    stale TMG copy. Where there are several, the TMG columns show the
    latest, since the record holds one of each. The agreement is the
    exception and is derived across all of them.
    """
    ae_tmg = get_latest_ae_tmg(ae_tmgs)
    values = {
        "ae_initial": ae_initial,
        "ae_initial_action_identifier": ae_initial.action_identifier,
        "ae_classification": ae_initial.ae_classification,
        "ae_classification_other": ae_initial.ae_classification_other or "",
        "investigator_ae_classification_agreed": (
            get_investigator_ae_classification_agreed(ae_initial, ae_tmgs)
        ),
    }
    if ae_tmg is None:
        values.update(
            {
                "ae_tmg": None,
                "ae_tmg_action_identifier": None,
                "investigator_ae_classification": None,
                "investigator_ae_classification_other": "",
            }
        )
    else:
        values.update(
            {
                "ae_tmg": ae_tmg,
                "ae_tmg_action_identifier": ae_tmg.action_identifier,
                "investigator_ae_classification": ae_tmg.investigator_ae_classification,
                "investigator_ae_classification_other": (
                    ae_tmg.investigator_ae_classification_other or ""
                ),
            }
        )
    return values


def get_original_ae_classification(
    ae_initial: "AeInitial",
) -> tuple[AeClassification | None, str]:
    """The original AE report's classification and its `other` text.

    Where the original says OTHER, the text is the classification. It
    resolves to a listed AeClassification where it names one, and is
    carried across as free text where it does not.
    """
    ae_classification_obj = ae_initial.ae_classification
    if ae_classification_obj is not None and ae_classification_obj.name == OTHER:
        ae_classification_other = ae_initial.ae_classification_other or NULL_STRING
        try:
            ae_classification_obj = AeClassification.objects.get(
                Q(name=ae_classification_other.lower())
                | Q(display_name=ae_classification_other)
            )
        except AeClassification.DoesNotExist:
            return ae_initial.ae_classification, ae_classification_other
        return ae_classification_obj, NULL_STRING
    return ae_classification_obj, NULL_STRING


def get_final_ae_classification(
    ae_initial: "AeInitial", ae_tmgs: "list[AeTmg]"
) -> tuple[AeClassification | None, str, str]:
    """Return the final classification, its `other` text and a review status.

    Until an AeTmg exists there is nothing to compare (`PENDING`). The
    classification is filled in only where every TMG report agrees with
    the original, in which case the original's is the answer.
    """
    if not ae_tmgs:
        return None, NULL_STRING, PENDING
    if get_investigator_ae_classification_agreed(ae_initial, ae_tmgs) == YES:
        ae_classification_obj, ae_classification_other = get_original_ae_classification(
            ae_initial
        )
        return ae_classification_obj, ae_classification_other, AGREED
    return None, NULL_STRING, REQUIRES_REVIEW


def get_refresh_values(
    afc: "AeFinalClassification",
    ae_initial: "AeInitial",
    ae_tmgs: "list[AeTmg]",
) -> dict:
    """Values a refresh would write to `afc`.

    `final_ae_classification` is offered only where the reviewer has
    not settled the record. `review_status` always refreshes: it
    describes the sources, not the answer.
    """
    values = get_ae_values_to_copy(ae_initial, ae_tmgs)
    final_obj, final_other, review_status = get_final_ae_classification(ae_initial, ae_tmgs)
    values["review_status"] = review_status
    if afc.conflict_resolved != YES:
        values["final_ae_classification"] = final_obj
        values["final_ae_classification_other"] = final_other
    return values


def refresh_copies_from_sources(
    afc: "AeFinalClassification",
    ae_initial: "AeInitial",
    ae_tmgs: "list[AeTmg]",
) -> list[str]:
    """Refresh `afc` from its source records.

    Returns the list of fields written, empty if nothing changed.
    """
    values = get_refresh_values(afc, ae_initial, ae_tmgs)
    changed = {f: v for f, v in values.items() if getattr(afc, f) != v}
    if not changed:
        return []
    for f, v in changed.items():
        setattr(afc, f, v)
    afc.save(update_fields=list(changed))
    return list(changed)


def resolution_is_stale(
    afc: "AeFinalClassification",
    ae_initial: "AeInitial",
    ae_tmgs: "list[AeTmg]",
) -> bool:
    """True where the sources have moved since the reviewer resolved.

    A settled record is not a discrepancy however far the reviewer's
    answer sits from the sources: they resolved against those values
    knowingly. Only a change since then puts the record back in front
    of them.
    """
    if afc.conflict_resolved != YES:
        return False
    ae_tmg = get_latest_ae_tmg(ae_tmgs)
    investigator_obj = ae_tmg.investigator_ae_classification if ae_tmg else None
    return (
        afc.resolved_ae_classification != ae_initial.ae_classification
        or afc.resolved_investigator_ae_classification != investigator_obj
    )


def limit_choices_to() -> dict:
    return {
        "name__in": [
            tpl[0]
            for tpl in AeClassification.objects.values_list("name").exclude(
                name=NOT_APPLICABLE
            )
        ]
    }


class AeFinalClassification(
    NonUniqueSubjectIdentifierModelMixin, SiteModelMixin, BaseUuidModel
):
    """An investigator form completed after study closure
    to capture an agreed final AE classification.
    """

    report_datetime = models.DateTimeField(default=timezone.now)

    final_ae_classification = models.ForeignKey(
        AeClassification,
        on_delete=models.PROTECT,
        verbose_name="Adverse Event (AE) Classification",
        null=True,
        blank=False,
        limit_choices_to=limit_choices_to,
    )

    final_ae_classification_other = OtherCharField(max_length=250)

    final_ae_classification_comment = models.TextField(
        max_length=250,
        verbose_name="Classification comment (if any)",
        help_text="May be left blank",
        default=NULL_STRING,
        blank=True,
    )

    verified = models.BooleanField(default=False, help_text="Field retired")

    conflict_resolved = models.CharField(
        verbose_name="Have you reviewed this record and settled the classification above?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "Once yes, the classification above is yours and is not revised by "
            "the backfill. You will be asked again if the source reports change."
        ),
    )

    review_status = models.CharField(
        verbose_name="Review status",
        max_length=25,
        choices=REVIEW_STATUS,
        default=PENDING,
        editable=False,
        help_text="Set from the source reports. Not editable.",
    )

    # the sources as they read when conflict_resolved was last set to YES
    resolved_ae_classification = models.ForeignKey(
        AeClassification,
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name="Original AE Classification, as reviewed",
        null=True,
        editable=False,
    )

    # the sources as they read when conflict_resolved was last set to YES
    resolved_investigator_ae_classification = models.ForeignKey(
        AeClassification,
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name="Investigator AE Classification, as reviewed",
        null=True,
        editable=False,
    )

    ae_initial = models.ForeignKey(AeInitial, on_delete=models.PROTECT, related_name="+")

    ae_initial_action_identifier = models.CharField(max_length=25, unique=True)

    # copied from meta_ae.aeinitial
    ae_classification = models.ForeignKey(
        AeClassification,
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name="Original AE Classification",
        help_text="Copied from original AE report",
    )

    # copied from meta_ae.aeinitial
    ae_classification_other = OtherCharField(
        verbose_name="Original AE Classification (Other)",
        max_length=250,
        help_text="Copied from original AE report",
    )

    ae_tmg = models.ForeignKey(
        AeTmg,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        help_text="May be null if no AE TMG report has been submitted yet.",
    )

    ae_tmg_action_identifier = models.CharField(
        max_length=25,
        unique=True,
        null=True,
        blank=True,
    )

    # copied from meta_ae.aetmg
    investigator_ae_classification_agreed = models.CharField(
        verbose_name=(
            "TMG investigator agrees with the AE classification from the original AE report?"
        ),
        max_length=15,
        choices=YES_NO,
        default=NULL_STRING,
    )

    # copied from meta_ae.aetmg
    investigator_ae_classification = models.ForeignKey(
        AeClassification,
        related_name="+",
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Investigator AE Classification",
        help_text="Copied from the AE TMG",
    )

    # copied from meta_ae.aetmg
    investigator_ae_classification_other = OtherCharField(
        verbose_name="Investigator AE Classification (Other)",
        max_length=250,
        help_text="Copied from the AE TMG",
        default=NULL_STRING,
    )

    objects = ModelManager()

    on_site = CurrentSiteManager()

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.subject_identifier}: AeInitial-{self.ae_initial}"

    def save(self, *args, update_fields=None, **kwargs):
        """Snapshot the sources the reviewer resolved against.

        Taken on a full save, so the admin, the shell and any import
        all record it. A save naming `update_fields`, as the backfill
        makes, leaves the snapshot alone unless it is itself changing
        `conflict_resolved`.
        """
        if update_fields is None or "conflict_resolved" in update_fields:
            self.update_resolved_snapshot()
            if update_fields is not None:
                update_fields = [*update_fields, *RESOLVED_SNAPSHOT_FIELDS]
        if update_fields is not None:
            # edc_sites tests for the key, not the value, so an explicit
            # update_fields=None is not the same as leaving it out
            kwargs["update_fields"] = update_fields
        super().save(*args, **kwargs)

    def update_resolved_snapshot(self) -> None:
        if self.conflict_resolved == YES:
            self.resolved_ae_classification = self.ae_classification
            self.resolved_investigator_ae_classification = self.investigator_ae_classification
        else:
            self.resolved_ae_classification = None
            self.resolved_investigator_ae_classification = None

    class Meta(BaseUuidModel.Meta):
        verbose_name = "AE Final Classification"
        verbose_name_plural = "AE Final Classification"
