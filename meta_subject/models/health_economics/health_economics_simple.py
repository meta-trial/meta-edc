from django.db import models
from edc_constants.choices import MARITAL_STATUS
from edc_he.model_mixins import HealthEconomicsEducationModelMixin
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfModelMixin


class HealthEconomicsSimple(HealthEconomicsEducationModelMixin, CrfModelMixin, BaseUuidModel):
    occupation = models.CharField(
        verbose_name="What is your occupation/profession?", max_length=50
    )

    marital_status = models.CharField(
        verbose_name="Marital status",
        max_length=25,
        choices=MARITAL_STATUS,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health Economics (M3)"
        verbose_name_plural = "Health Economics (M3)"
