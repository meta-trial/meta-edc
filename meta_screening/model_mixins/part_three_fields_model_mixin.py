from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import (
    NO,
    YES_NO,
    YES_NO_NA,
    YES_NO_PENDING_NA_GLUCOSE_SCREENING,
)
from edc_constants.constants import NOT_APPLICABLE
from edc_glucose.model_mixins import (
    fasting_model_mixin_factory,
    fbg_model_mixin_factory,
    ogtt_model_mixin_factory,
)
from edc_lab.choices import GLUCOSE_UNITS, SERUM_CREATININE_UNITS
from edc_vitals.model_mixins import (
    BloodPressureModelMixin,
    SimpleBloodPressureModelMixin,
    WeightHeightBmiModelMixin,
)

from .creatinine_fields_model_mixin import CreatinineModelFieldsMixin


class FastingModelMixin(
    fasting_model_mixin_factory(),
    fasting_model_mixin_factory(
        "repeat",
        repeat_fasting=models.CharField(
            verbose_name="Has the participant fasted?",
            max_length=15,
            choices=YES_NO_NA,
            blank=False,
            default=NOT_APPLICABLE,
            help_text="As reported by patient",
        ),
    ),
):
    class Meta:
        abstract = True


class FbgModelMixin(
    fbg_model_mixin_factory(
        "fbg",
        fbg_units=models.CharField(
            verbose_name="FBG units",
            max_length=15,
            choices=GLUCOSE_UNITS,
            null=True,
            blank=True,
        ),
    ),
    fbg_model_mixin_factory(
        "fbg2",
        fbg2_units=models.CharField(
            verbose_name="FBG units",
            max_length=15,
            choices=GLUCOSE_UNITS,
            null=True,
            blank=True,
        ),
    ),
):
    class Meta:
        abstract = True


class OgttModelMixin(
    ogtt_model_mixin_factory(
        "ogtt",
        ogtt_units=models.CharField(
            verbose_name="OGTT Units",
            max_length=15,
            choices=GLUCOSE_UNITS,
            null=True,
            blank=True,
        ),
    ),
    ogtt_model_mixin_factory(
        "ogtt2",
        ogtt2_units=models.CharField(
            verbose_name="Repeat OGTT Units",
            max_length=15,
            choices=GLUCOSE_UNITS,
            null=True,
            blank=True,
        ),
    ),
    models.Model,
):
    class Meta:
        abstract = True


class PartThreeFieldsModelMixin(
    FastingModelMixin,
    FbgModelMixin,
    OgttModelMixin,
    CreatinineModelFieldsMixin,
    BloodPressureModelMixin,
    SimpleBloodPressureModelMixin,
    WeightHeightBmiModelMixin,
    models.Model,
):

    repeat_glucose_opinion = models.CharField(
        verbose_name=(
            "In opinion of the clinician, " "should the glucose measurements be repeated?"
        ),
        max_length=15,
        choices=YES_NO,
        default=NO,
        help_text=(
            "If repeated, must be at least 3 days "
            "after the first glucose measures (FBG, OGTT)"
        ),
    )

    repeat_appt_datetime = models.DateTimeField(
        verbose_name="Appointment date for repeat glucose testing",
        null=True,
        blank=True,
        help_text="must be at least 3 days after the first glucose measures (FBG, OGTT)",
    )

    repeat_glucose_performed = models.CharField(
        verbose_name="Were the glucose measurements repeated?",
        max_length=15,
        choices=YES_NO_PENDING_NA_GLUCOSE_SCREENING,
        default=NOT_APPLICABLE,
        help_text="Select YES when you are ready to enter the repeat results",
    )

    creatinine_units = models.CharField(
        verbose_name="Units (creatinine)",
        max_length=15,
        choices=SERUM_CREATININE_UNITS,
        null=True,
        blank=True,
    )

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

    hba1c_datetime = models.DateTimeField(
        verbose_name="HbA1c date and time",
        null=True,
        blank=True,
        help_text="Date and time of result.",
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

    @admin.display(description="P3 repeat appt", ordering="repeat_appt_datetime")
    def p3_repeat_appt(self):
        return self.repeat_appt_datetime

    class Meta:
        abstract = True
