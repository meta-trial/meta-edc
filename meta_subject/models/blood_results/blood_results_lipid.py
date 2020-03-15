from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from edc_constants.choices import YES_NO
from edc_crf.model_mixins import CrfNoManagerModelMixin
from edc_model.models import BaseUuidModel
from edc_model.validators import datetime_not_future
from edc_reportable.choices import REPORTABLE
from edc_reportable.units import MILLIMOLES_PER_LITER
from edc_reportable.model_mixin import BloodResultsModelMixin

from ...constants import BLOOD_RESULTS_LIPID_ACTION
from ..subject_requisition import SubjectRequisition


class BloodResultsLipid(CrfNoManagerModelMixin, BloodResultsModelMixin, BaseUuidModel):

    action_name = BLOOD_RESULTS_LIPID_ACTION

    tracking_identifier_prefix = "LP"

    lipid_requisition = models.ForeignKey(
        SubjectRequisition,
        on_delete=PROTECT,
        related_name="lipid",
        verbose_name="Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit",
    )

    lipid_assay_datetime = models.DateTimeField(
        verbose_name="Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    # ldl
    ldl = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        verbose_name="LDL",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    ldl_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER),),
        null=True,
        blank=True,
    )

    ldl_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    ldl_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # hdl
    hdl = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        verbose_name="HDL",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    hdl_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER),),
        null=True,
        blank=True,
    )

    hdl_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    hdl_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # trig
    trig = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        verbose_name="Triglycerides",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    trig_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER),),
        null=True,
        blank=True,
    )

    trig_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    trig_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta(CrfNoManagerModelMixin.Meta):
        verbose_name = "Blood Result: Lipids"
        verbose_name_plural = "Blood Results: Lipids"
