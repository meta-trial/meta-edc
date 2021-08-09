from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import NO, YES_NO
from edc_glucose.model_mixins import FastingModelMixin, IfgModelMixin, OgttModelMixin
from edc_vitals.model_mixins import (
    BloodPressureModelMixin,
    SimpleBloodPressureModelMixin,
    WeightHeightBmiModelMixin,
)

from .creatinine_fields_model_mixin import CreatinineModelFieldsMixin


class PartThreeFieldsModelMixin(
    FastingModelMixin,
    IfgModelMixin,
    OgttModelMixin,
    CreatinineModelFieldsMixin,
    BloodPressureModelMixin,
    SimpleBloodPressureModelMixin,
    WeightHeightBmiModelMixin,
    models.Model,
):

    part_three_report_datetime = models.DateTimeField(
        verbose_name="Part 3 report date and time",
        null=True,
        blank=False,
        help_text="Date and time of report.",
    )

    waist_circumference = models.DecimalField(
        verbose_name="Waist circumference",
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(50.0), MaxValueValidator(175.0)],
        null=True,
        blank=True,
        help_text="in centimeters",
    )

    hba1c_performed = models.CharField(
        verbose_name="Was the HbA1c performed?",
        max_length=15,
        choices=YES_NO,
        default=NO,
        help_text="",
    )

    hba1c_value = models.DecimalField(
        verbose_name="HbA1c",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="in %",
    )

    creatinine_performed = models.CharField(
        verbose_name="Was the serum creatinine performed?",
        max_length=15,
        choices=YES_NO,
        default=NO,
        help_text="",
    )

    class Meta:
        abstract = True
