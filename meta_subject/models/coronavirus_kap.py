from edc_crf.model_mixins import CrfModelMixin
from edc_model import models as edc_models

from sarscov2.model_mixins import CoronaKapModelMixin, CoronaKapDiseaseModelMixin


class CoronaKap(
    CrfModelMixin,
    CoronaKapDiseaseModelMixin,
    CoronaKapModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(CrfModelMixin.Meta):
        verbose_name = "Coronavirus Knowledge, Attitudes, and Practices"
        verbose_name_plural = "Coronavirus Knowledge, Attitudes, and Practices"
