from clinicedc_constants import NOT_APPLICABLE, NULL_STRING
from clinicedc_constants.choices import YES_NO
from django.db import models
from django.utils import timezone
from edc_adverse_event.models import AeClassification
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model_fields.fields import OtherCharField
from edc_sites.managers import CurrentSiteManager
from edc_sites.model_mixins import SiteModelMixin

from .ae_initial import AeInitial
from .ae_tmg import AeTmg

CLASSIFICATION_TRIGGER_FIELDS = (
    "ae_classification",
    "investigator_ae_classification",
)


class ModelManager(models.Manager):
    use_in_migrations = True


def get_ae_values_to_copy(ae_initial: "AeInitial", ae_tmg: "AeTmg | None") -> dict:
    """Values that AeFinalClassification copies from the source reports.

    `tmg` is optional: an AeInitial may exist without a corresponding
    AeTmg. In that case only the AeInitial-side fields are returned,
    and the ae_tmg-side fields are nulled so a subsequent refresh
    clears any stale TMG copy.
    """
    values = {
        "ae_initial": ae_initial,
        "ae_initial_action_identifier": ae_initial.action_identifier,
        "ae_classification": ae_initial.ae_classification,
        "ae_classification_other": ae_initial.ae_classification_other or "",
    }
    if ae_tmg is None:
        values.update(
            {
                "ae_tmg": None,
                "ae_tmg_action_identifier": None,
                "investigator_ae_classification_agreed": "",
                "investigator_ae_classification": None,
                "investigator_ae_classification_other": "",
            }
        )
    else:
        values.update(
            {
                "ae_tmg": ae_tmg,
                "ae_tmg_action_identifier": ae_tmg.action_identifier,
                "investigator_ae_classification_agreed": (ae_tmg.original_report_agreed),
                "investigator_ae_classification": ae_tmg.investigator_ae_classification,
                "investigator_ae_classification_other": (
                    ae_tmg.investigator_ae_classification_other or ""
                ),
            }
        )
    return values


def refresh_copies_from_sources(
    afc: "AeFinalClassification",
    ae_initial: "AeInitial",
    ae_tmg: "AeTmg | None",
) -> list[str]:
    """Refresh copy fields on `afc` from its source records.

    If `ae_classification` (on AeInitial) or `investigator_ae_classification`
    (on AeTmg) changed, also clears `afc.final_ae_classification` so the
    investigator is forced to reassess. Returns the list of fields written
    (empty list if nothing changed).
    """
    values = get_ae_values_to_copy(ae_initial, ae_tmg)
    changed = {f: v for f, v in values.items() if getattr(afc, f) != v}
    if not changed:
        return []
    classification_changed = any(f in changed for f in CLASSIFICATION_TRIGGER_FIELDS)
    if classification_changed and afc.final_ae_classification_id is not None:
        changed["final_ae_classification"] = None
        changed["final_ae_classification_other"] = NULL_STRING
        changed["verified"] = False
    for f, v in changed.items():
        setattr(afc, f, v)
    afc.save(update_fields=list(changed))
    return list(changed)


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

    verified = models.BooleanField(default=False)

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

    class Meta(BaseUuidModel.Meta):
        verbose_name = "AE Final Classification"
        verbose_name_plural = "AE Final Classification"
