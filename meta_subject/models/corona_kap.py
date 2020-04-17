from edc_crf.model_mixins import CrfModelMixin
from edc_model import models as edc_models

from sarscov2.model_mixins import CoronaKapModelMixin


class CoronaKap(CrfModelMixin, CoronaKapModelMixin, edc_models.BaseUuidModel):
    class Meta:
        verbose_name = "Corona Knowledge, Attitudes, and Practices"
        verbose_name_plural = "Corona Knowledge, Attitudes, and Practices"
