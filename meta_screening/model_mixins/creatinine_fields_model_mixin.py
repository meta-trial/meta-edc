from django.db import models
from edc_constants.constants import NOT_APPLICABLE
from edc_lab.choices import SERUM_CREATININE_UNITS_NA


class CreatinineModelFieldsMixin(models.Model):

    creatinine_value = models.DecimalField(
        verbose_name="Creatinine level",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    creatinine_units = models.CharField(
        verbose_name="Units (creatinine)",
        max_length=15,
        choices=SERUM_CREATININE_UNITS_NA,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True
