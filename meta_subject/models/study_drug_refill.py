from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class StudyDrugRefill(CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Study Drug Refill"
        verbose_name_plural = "Study Drug Refills"
