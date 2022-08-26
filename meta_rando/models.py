from django.db import models
from edc_constants.choices import GENDER
from edc_model import models as edc_models
from edc_randomization.model_mixins import RandomizationListModelMixin


class RandomizationList(RandomizationListModelMixin, edc_models.BaseUuidModel):

    gender = models.CharField(max_length=25, choices=GENDER)

    class Meta(RandomizationListModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Randomization List (Phase Three)"
        verbose_name_plural = "Randomization List (Phase Three)"
