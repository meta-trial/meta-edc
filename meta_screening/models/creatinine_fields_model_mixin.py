from django.db import models
from django.utils.safestring import mark_safe
from meta_screening.choices import SERUM_CREATININE_UNITS


class CreatinineModelFieldsMixin(models.Model):

    creatinine = models.DecimalField(
        verbose_name=mark_safe("Creatinine <u>level</u>"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    creatinine_units = models.CharField(
        verbose_name="Units (creatinine)",
        max_length=15,
        choices=SERUM_CREATININE_UNITS,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
