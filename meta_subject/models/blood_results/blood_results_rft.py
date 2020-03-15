from django.db import models
from django.db.models.deletion import PROTECT
from edc_constants.choices import YES_NO
from edc_crf.model_mixins import CrfNoManagerModelMixin
from edc_model.models import BaseUuidModel
from edc_model.validators import datetime_not_future
from edc_reportable import MILLIGRAMS_PER_DECILITER, MILLIMOLES_PER_LITER
from edc_reportable.choices import REPORTABLE
from edc_reportable.model_mixin import BloodResultsModelMixin
from meta_screening.models import CreatinineModelFieldsMixin

from ...constants import BLOOD_RESULTS_RFT_ACTION
from ..subject_requisition import SubjectRequisition


class BloodResultsRft(
    CrfNoManagerModelMixin,
    BloodResultsModelMixin,
    CreatinineModelFieldsMixin,
    BaseUuidModel,
):

    action_name = BLOOD_RESULTS_RFT_ACTION

    tracking_identifier_prefix = "RF"

    rft_requisition = models.ForeignKey(
        SubjectRequisition,
        on_delete=PROTECT,
        related_name="ft",
        verbose_name="Requisition",
        null=True,
        blank=True,
        help_text=(
            "Start typing the requisition identifier or select one from this visit"
        ),
    )

    rft_assay_datetime = models.DateTimeField(
        verbose_name="Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    # Serum urea levels
    urea = models.DecimalField(
        verbose_name="Urea (BUN)", decimal_places=2, max_digits=6, null=True, blank=True
    )

    urea_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER),),
        null=True,
        blank=True,
    )

    urea_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    urea_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # Serum creatinine levels
    # note, two fields not shown are from the model mixin

    creatinine_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    creatinine_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # Serum uric acid levels
    uric_acid = models.DecimalField(
        verbose_name="Uric Acid", decimal_places=4, max_digits=10, null=True, blank=True
    )

    uric_acid_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=(
            (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER),
            (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
        ),
        null=True,
        blank=True,
    )

    uric_acid_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    uric_acid_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # eGFR
    egfr = models.DecimalField(
        verbose_name="eGFR",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="mL/min/1.73 m2 (system calculated)",
    )

    class Meta(CrfNoManagerModelMixin.Meta):
        verbose_name = "Blood Result: RFT"
        verbose_name_plural = "Blood Results: RFT"
