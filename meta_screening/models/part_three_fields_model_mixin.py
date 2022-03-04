from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import NO, YES_NO, YES_NO_PENDING_NA, YES_NO_UNSURE
from edc_constants.constants import NOT_APPLICABLE
from edc_glucose.model_mixins import (
    FastingModelMixin,
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

# TODO: repeat FBG and OGTT after 48-72 hours if response to fasting is unsure in opinion of the clinician (PART 4)


class FastingModelMixin(
    fasting_model_mixin_factory(),
    fasting_model_mixin_factory(
        "repeat",
        repeat_fasting=models.CharField(
            verbose_name="Has the participant fasted?",
            max_length=15,
            choices=YES_NO,
            null=True,
            blank=True,
            help_text="As reported by patient",
        ),
    ),
):
    class Meta:
        abstract = True


class FbgModelMixin(
    fbg_model_mixin_factory(
        "ifg",
        ifg_units=models.CharField(
            verbose_name="IFG units",
            max_length=15,
            choices=GLUCOSE_UNITS,
            null=True,
            blank=True,
        ),
    ),
    fbg_model_mixin_factory(
        "ifg2",
        ifg2_units=models.CharField(
            verbose_name="IFG units",
            max_length=15,
            choices=GLUCOSE_UNITS,
            null=True,
            blank=True,
        ),
    ),
):
    # added 19/11/2021
    fasting_opinion = models.CharField(
        verbose_name="In the opinion of the clinican, has the participant fasted?",
        max_length=15,
        choices=YES_NO_UNSURE,
        null=True,
        blank=False,
    )

    repeat_fasting_opinion = models.CharField(
        verbose_name="In the opinion of the clinican, has the participant fasted for these repeat glucose measurement?",
        max_length=15,
        choices=YES_NO_UNSURE,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class OgttModelMixin(
    ogtt_model_mixin_factory(
        "ogtt",
        ogtt_units=models.CharField(
            verbose_name="Units (OGTT)",
            max_length=15,
            choices=GLUCOSE_UNITS,
            null=True,
            blank=True,
        ),
    ),
    ogtt_model_mixin_factory(
        "ogtt2",
        ogtt2_units=models.CharField(
            verbose_name="Units (Repeat OGTT)",
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

    lower_bmi_value = 13.0

    # TODO: NO and UNSURE means dont test, come back later

    repeat_glucose_opinion = models.CharField(
        verbose_name="In opinion of the clinician, should the glucose measurements be repeated?",
        max_length=15,
        choices=YES_NO,
        default=NO,
        help_text="If to be repeated, do so at least 3 days after the first OGTT",
    )

    repeat_glucose_performed = models.CharField(
        verbose_name="Were the glucose measurements repeated?",
        max_length=15,
        choices=YES_NO_PENDING_NA,
        default=NOT_APPLICABLE,
        help_text="If repeated, must be at least 3 days after the first glucose measures (FBG, OGTT)",
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
