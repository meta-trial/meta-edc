from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import NO, YES_NO
from edc_glucose.model_mixins import FastingModelMixin, IfgModelMixin, OgttModelMixin
from edc_model import models as edc_models

from .creatinine_fields_model_mixin import CreatinineModelFieldsMixin


class PartThreeFieldsModelMixin(
    FastingModelMixin,
    IfgModelMixin,
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

    sys_blood_pressure = edc_models.SystolicPressureField(
        null=True,
        blank=True,
    )

    dia_blood_pressure = edc_models.DiastolicPressureField(
        null=True,
        blank=True,
    )

    severe_htn = models.CharField(
        verbose_name="Does the patient have severe hypertension?",
        max_length=15,
        choices=YES_NO,
        help_text="BP > 180/120mmHg",
        null=True,
        blank=True,
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

    # haemoglobin_value = models.DecimalField(
    #     decimal_places=1,
    #     max_digits=6,
    #     null=True,
    #     blank=True,
    #     help_text=f"in {GRAMS_PER_DECILITER}",
    # )
    #
    # wbc_value = models.DecimalField(
    #     verbose_name="WBC",
    #     decimal_places=2,
    #     max_digits=6,
    #     null=True,
    #     blank=True,
    #     help_text=f"in {TEN_X_9_PER_LITER}",
    # )
    #
    # ast_value = models.IntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(999)],
    #     verbose_name="AST",
    #     null=True,
    #     blank=True,
    #     help_text=f"in {IU_LITER_DISPLAY}",
    # )
    #
    # alt_value = models.IntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(999)],
    #     verbose_name="ALT",
    #     null=True,
    #     blank=True,
    #     help_text=f"in {IU_LITER_DISPLAY}",
    # )
    #
    # ggt_value = models.IntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(999)],
    #     verbose_name="GGT",
    #     null=True,
    #     blank=True,
    #     help_text=f"in {IU_LITER_DISPLAY}",
    # )
    #
    # albumin_value = models.DecimalField(
    #     decimal_places=1,
    #     max_digits=6,
    #     validators=[MinValueValidator(1), MaxValueValidator(999)],
    #     verbose_name="Serum Albumin",
    #     null=True,
    #     blank=True,
    #     help_text=f"in {GRAMS_PER_LITER}",
    # )
    #
    # alp_value = models.IntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(999)],
    #     verbose_name="ALP",
    #     null=True,
    #     blank=True,
    #     help_text=f"in {IU_LITER_DISPLAY}",
    # )

    class Meta:
        abstract = True
