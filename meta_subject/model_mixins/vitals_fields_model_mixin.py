from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_vitals.models import WeightField


class VitalsFieldsModelMixin(models.Model):

    weight = WeightField(null=True)

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
