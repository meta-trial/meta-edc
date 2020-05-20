from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_constants.choices import YES_NO, NO
from edc_model import models as edc_models

from .creatinine_fields_model_mixin import CreatinineModelFieldsMixin
from .model_mixins import FastingModelMixin, OgttModelMixin, FastingGlucoseModelMixin


class PartThreeFieldsModelMixin(
    FastingModelMixin,
    FastingGlucoseModelMixin,
    OgttModelMixin,
    CreatinineModelFieldsMixin,
    models.Model,
):

    part_three_report_datetime = models.DateTimeField(
        verbose_name="Second stage report date and time",
        null=True,
        blank=False,
        help_text="Date and time of report.",
    )

    sys_blood_pressure = edc_models.SystolicPressureField(null=True, blank=True,)

    dia_blood_pressure = edc_models.DiastolicPressureField(null=True, blank=True,)

    weight = edc_models.WeightField(null=True, blank=True)

    height = edc_models.HeightField(null=True, blank=True)

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

    hba1c = models.DecimalField(
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
