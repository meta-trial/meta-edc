from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO
from edc_model.models import BaseUuidModel
from edc_vitals.model_mixins import (
    BloodPressureModelMixin,
    SimpleBloodPressureModelMixin,
)

from ..model_mixins import CrfModelMixin, VitalsFieldsModelMixin


class PhysicalExam(
    SimpleBloodPressureModelMixin,
    BloodPressureModelMixin,
    VitalsFieldsModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    irregular_heartbeat = models.CharField(
        verbose_name=mark_safe("Is the heart beat <u>irregular</u>?"),  # nosec B308
        max_length=15,
        choices=YES_NO,
    )

    irregular_heartbeat_description = models.TextField(
        "If the heartbeat is <u>irregular</u>, please describe", default="", blank=True
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

    jaundice = models.CharField(verbose_name="Jaundice?", max_length=15, choices=YES_NO)

    peripheral_oedema = models.CharField(
        verbose_name="Presence of peripheral oedema?", max_length=15, choices=YES_NO
    )

    abdominal_tenderness = models.CharField(
        verbose_name="Abdominal tenderness on palpation?", max_length=15, choices=YES_NO
    )

    abdominal_tenderness_description = models.TextField(
        verbose_name="If YES, abdominal tenderness, please describe",
        default="",
        blank=True,
    )

    enlarged_liver = models.CharField(
        verbose_name="Enlarged liver on palpation?", max_length=15, choices=YES_NO
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Physical Exam"
        verbose_name_plural = "Physical Exams"
