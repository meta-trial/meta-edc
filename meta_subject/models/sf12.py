from edc_model import models as edc_models
from edc_qol.model_mixins import Sf12ModelMixin

from ..model_mixins import CrfModelMixin


class Sf12(Sf12ModelMixin, CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(Sf12ModelMixin.Meta, CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        pass


# TODO: add proxy model and two options Swahili and English
