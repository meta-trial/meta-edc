from django.db import models
from edc_model import models as edc_models

from .model_mixins import CrfModelMixin


class AdditionalScreening(CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Additional Screening"
        verbose_name_plural = "Additional Screening"
