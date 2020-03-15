from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO, NO
from edc_lab.choices import RESULT_QUANTIFIER
from edc_lab.constants import EQ
from edc_model import models as edc_models
from edc_model.validators import hm_validator

from ..choices import GLUCOSE_UNITS
from .creatinine_fields_model_mixin import CreatinineModelFieldsMixin


class PartThreeFieldsModelMixin(CreatinineModelFieldsMixin, models.Model):

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

    fasted = models.CharField(
        verbose_name="Has the participant fasted?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    fasted_duration_str = models.CharField(
        verbose_name="How long have they fasted in hours and/or minutes?",
        max_length=8,
        validators=[hm_validator],
        null=True,
        blank=True,
        help_text="Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
    )

    fasted_duration_minutes = models.IntegerField(
        null=True, help_text="system calculated value"
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

    # IFG
    fasting_glucose = models.DecimalField(
        verbose_name=mark_safe("Fasting glucose <u>level</u>"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    fasting_glucose_quantifier = models.CharField(
        max_length=10, choices=RESULT_QUANTIFIER, default=EQ,
    )

    fasting_glucose_units = models.CharField(
        verbose_name="Units (fasting glucose)",
        max_length=15,
        choices=GLUCOSE_UNITS,
        blank=True,
        null=True,
    )

    fasting_glucose_datetime = models.DateTimeField(
        verbose_name=mark_safe("<u>Time</u> fasting glucose <u>level</u> measured"),
        null=True,
        blank=True,
    )

    ogtt_base_datetime = models.DateTimeField(
        verbose_name=mark_safe("<u>Time</u> oral glucose solution was given"),
        null=True,
        blank=True,
        help_text="(glucose solution given)",
    )

    ogtt_two_hr = models.DecimalField(
        verbose_name=mark_safe(
            "Blood glucose <u>level</u> 2-hours " "after oral glucose solution given"
        ),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    ogtt_two_hr_quantifier = models.CharField(
        max_length=10, choices=RESULT_QUANTIFIER, default=EQ,
    )

    ogtt_two_hr_units = models.CharField(
        verbose_name="Units (Blood glucose 2hrs after...)",
        max_length=15,
        choices=GLUCOSE_UNITS,
        blank=True,
        null=True,
    )

    ogtt_two_hr_datetime = models.DateTimeField(
        verbose_name=mark_safe(
            "<u>Time</u> blood glucose measured 2-hours "
            "after oral glucose solution given"
        ),
        blank=True,
        null=True,
        help_text="(2 hours after glucose solution given)",
    )

    class Meta:
        abstract = True
