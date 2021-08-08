from django.db import models
from edc_model import models as edc_models

from ..model_mixins import ArvRegimenHistoryDetailModelMixin, CrfModelMixin


class OtherArvRegimens(CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Other ARV Regimens"
        verbose_name_plural = "Other ARV Regimens"


class OtherArvRegimensDetail(
    ArvRegimenHistoryDetailModelMixin, edc_models.BaseUuidModel
):

    arv_history = models.ForeignKey(OtherArvRegimens)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Other ARV Regimens Detail"
        verbose_name_plural = "Other ARV Regimens Detail"
