from django.contrib.sites.managers import CurrentSiteManager as DjangoCurrentSiteManager
from django.db import models
from django.db.models import Manager
from edc_constants.constants import EQ
from edc_lab.choices import RESULT_QUANTIFIER
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_reportable import (
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MILLIMOLES_PER_LITER_DISPLAY,
    PERCENT,
)
from edc_sites.model_mixins import SiteModelMixin

from .dm_diagnosis import DmDiagnosis

UTESTIDS = (("fbg", "FBG mmol/L"), ("ogtt", "OGTT mmol/L"), ("hba1c", "HbA1c %"))
UNITS = (
    (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
    (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER_DISPLAY),
    (PERCENT, "%"),
)


class DmDxResult(SiteModelMixin, BaseUuidModel):
    """A user inline model to capture results used in determining a diagnosis
    of diabetes (in the context of this study).

    Glucose values (FBG/OGTT) are in mmol/L.
    """

    dm_diagnosis = models.ForeignKey(DmDiagnosis, on_delete=models.PROTECT)

    report_date = models.DateField(verbose_name="Date")

    utestid = models.CharField(
        verbose_name="Test",
        max_length=15,
        choices=UTESTIDS,
    )

    quantifier = models.CharField(
        max_length=10,
        choices=RESULT_QUANTIFIER,
        default=EQ,
    )

    value = models.DecimalField(max_digits=8, decimal_places=2)

    units = models.CharField(
        verbose_name="Units",
        max_length=15,
        choices=UNITS,
    )

    fasted = models.BooleanField(
        verbose_name="Fasted?",
        max_length=15,
        default=False,
    )

    comment = models.CharField(max_length=35, null=True, blank=True)

    objects = Manager()
    on_site = DjangoCurrentSiteManager()
    history = HistoricalRecords()

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Diabetes diagnosis: Result"
        verbose_name_plural = "Diabetes diagnosis: Results"
