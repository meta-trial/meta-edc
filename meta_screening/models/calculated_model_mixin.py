from django.db import models
from edc_constants.choices import YES_NO_TBD
from edc_constants.constants import TBD
from edc_reportable.units import MICROMOLES_PER_LITER_DISPLAY, MILLIMOLES_PER_LITER


class CalculatedModelMixin(models.Model):

    # calculated
    calculated_egfr_value = models.DecimalField(
        verbose_name="eGFR",
        max_digits=8,
        decimal_places=4,
        null=True,
        help_text="mL/min/1.73m2 (system calculated)",
    )

    # converted if necessary
    converted_creatinine_value = models.DecimalField(
        verbose_name="Serum creatinine",
        max_digits=8,
        decimal_places=4,
        null=True,
        help_text=f"{MICROMOLES_PER_LITER_DISPLAY} (system converted)",
    )

    # converted if necessary
    converted_fbg_value = models.DecimalField(
        verbose_name="FBG level",
        max_digits=8,
        decimal_places=4,
        null=True,
        help_text=f"{MILLIMOLES_PER_LITER} (system converted)",
    )

    converted_fbg2_value = models.DecimalField(
        verbose_name="Repeat FBG level",
        max_digits=8,
        decimal_places=4,
        null=True,
        help_text=f"{MILLIMOLES_PER_LITER} (system converted)",
    )

    # converted if necessary
    converted_ogtt_value = models.DecimalField(
        verbose_name="OGTT (2-hours)",
        max_digits=8,
        decimal_places=4,
        null=True,
        help_text=f"{MILLIMOLES_PER_LITER} (system converted)",
    )

    # converted if necessary
    converted_ogtt2_value = models.DecimalField(
        verbose_name="Repeat OGTT (2-hours)",
        max_digits=8,
        decimal_places=4,
        null=True,
        help_text=f"{MILLIMOLES_PER_LITER} (system converted)",
    )

    # calculated
    inclusion_a = models.CharField(
        verbose_name="BMI>30 combined with FBG (6.1 to 6.9 mmol/L)",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        help_text="system calculated",
    )

    # calculated
    inclusion_b = models.CharField(
        verbose_name="BMI>30 combined with OGTT (2 hours) (7.0 to 11.10 mmol/L)",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        help_text="system calculated",
    )

    # calculated
    inclusion_c = models.CharField(
        verbose_name="BMI<=30 combined with FBG (6.3 to 6.9 mmol/L)",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        help_text="system calculated",
    )

    # calculated
    inclusion_d = models.CharField(
        verbose_name="BMI<=30 combined with OGTT (2 hours) (9.0 to 11.10 mmol/L)",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        help_text="system calculated",
    )

    class Meta:
        abstract = True
