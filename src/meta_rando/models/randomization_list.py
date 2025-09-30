from django.db import models
from edc_constants.choices import GENDER
from edc_model.models import BaseUuidModel
from edc_randomization.model_mixins import RandomizationListModelMixin


class RandomizationList(RandomizationListModelMixin, BaseUuidModel):
    gender = models.CharField(max_length=25, choices=GENDER)

    class Meta(RandomizationListModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Randomization List (Phase Three)"
        verbose_name_plural = "Randomization List (Phase Three)"
