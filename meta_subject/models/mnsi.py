from edc_mnsi.model_mixins import MnsiModelMixin
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class Mnsi(
    MnsiModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(MnsiModelMixin.Meta, CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        pass
