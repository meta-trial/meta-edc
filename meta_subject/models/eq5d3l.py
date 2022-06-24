from edc_model import models as edc_models
from edc_qol.model_mixins import Eq5d3lModelMixin

from ..model_mixins import CrfModelMixin


class Eq5d3l(
    Eq5d3lModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(Eq5d3lModelMixin.Meta, CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        pass
