from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from edc_constants.choices import YES_NO
from edc_crf.model_mixins import CrfNoManagerModelMixin
from edc_model.models import BaseUuidModel
from edc_model.validators import datetime_not_future
from edc_reportable import (
    IU_LITER,
    GRAMS_PER_LITER,
    IU_LITER_DISPLAY,
    GRAMS_PER_DECILITER,
)
from edc_reportable.choices import REPORTABLE
from edc_reportable.model_mixin import BloodResultsModelMixin

from ...constants import BLOOD_RESULTS_LFT_ACTION
from ..subject_requisition import SubjectRequisition


class BloodResultsLft(CrfNoManagerModelMixin, BloodResultsModelMixin, BaseUuidModel):
    action_name = BLOOD_RESULTS_LFT_ACTION

    tracking_identifier_prefix = "LF"

    lft_requisition = models.ForeignKey(
        SubjectRequisition,
        on_delete=PROTECT,
        related_name="lft",
        verbose_name="Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit",
    )

    lft_assay_datetime = models.DateTimeField(
        verbose_name="Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    # AST
    ast = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        verbose_name="AST",
        null=True,
        blank=True,
    )

    ast_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((IU_LITER, IU_LITER_DISPLAY),),
        null=True,
        blank=True,
    )

    ast_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    ast_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # AST
    alt = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        verbose_name="ALT",
        null=True,
        blank=True,
    )

    alt_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((IU_LITER, IU_LITER_DISPLAY),),
        null=True,
        blank=True,
    )

    alt_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    alt_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # ALP
    alp = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        verbose_name="ALP",
        null=True,
        blank=True,
    )

    alp_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((IU_LITER, IU_LITER_DISPLAY),),
        null=True,
        blank=True,
    )

    alp_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    alp_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # Serum Amylase
    amylase = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        verbose_name="Serum Amylase",
        null=True,
        blank=True,
    )

    amylase_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((IU_LITER, IU_LITER_DISPLAY),),
        null=True,
        blank=True,
    )

    amylase_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    amylase_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # Serum GGT
    ggt = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        verbose_name="GGT",
        null=True,
        blank=True,
    )

    ggt_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((IU_LITER, IU_LITER_DISPLAY),),
        null=True,
        blank=True,
    )

    ggt_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    ggt_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # Serum Albumin
    albumin = models.DecimalField(
        decimal_places=1,
        max_digits=6,
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        verbose_name="Serum Albumin",
        null=True,
        blank=True,
    )

    albumin_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=(
            (GRAMS_PER_DECILITER, GRAMS_PER_DECILITER),
            (GRAMS_PER_LITER, GRAMS_PER_LITER),
        ),
        null=True,
        blank=True,
    )

    albumin_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    albumin_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta(CrfNoManagerModelMixin.Meta):
        verbose_name = "Blood Result: LFT"
        verbose_name_plural = "Blood Results: LFT"
