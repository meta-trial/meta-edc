from clinicedc_constants import NO
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_vitals.models import WeightField


class VitalsFieldsModelMixin(models.Model):
    weight = WeightField(null=True)

    waist_circumference_measured = models.CharField(
        verbose_name="Was the patient's waist circumference measured today?",
        max_length=15,
        choices=YES_NO,
        help_text=(
            "Waist circumference may be provided at anytime "
            "but is required at 36 and 48 months"
        ),
        default=NO,
    )

    waist_circumference = models.DecimalField(
        verbose_name="Waist circumference",
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(50.0), MaxValueValidator(175.0)],
        help_text="in centimeters",
        null=True,
        blank=True,
    )

    waist_circumference_comment = models.TextField(
        verbose_name="If waist circumference not measured, please explain ...",
        help_text=(
            "A reason not measured may be provided at anytime "
            "but is required at 36 and 48 months"
        ),
        default="",
        blank=True,
    )

    # 10
    heart_rate = models.IntegerField(
        verbose_name="Heart rate:",
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        help_text="BPM",
    )

    # 11
    respiratory_rate = models.IntegerField(
        verbose_name="Respiratory rate:",
        validators=[MinValueValidator(6), MaxValueValidator(50)],
        help_text="breaths/min",
        null=True,
        blank=True,
    )

    # 12
    oxygen_saturation = models.IntegerField(
        verbose_name="Oxygen saturation:",
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        help_text="%",
        null=True,
        blank=True,
    )

    temperature = models.DecimalField(
        verbose_name="Temperature:",
        validators=[MinValueValidator(30), MaxValueValidator(45)],
        decimal_places=1,
        max_digits=3,
        help_text="in degrees Celcius",
    )

    class Meta:
        abstract = True
