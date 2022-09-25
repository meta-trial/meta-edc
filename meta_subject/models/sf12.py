from edc_model.models import BaseUuidModel
from edc_qol.model_mixins import Sf12ModelMixin

from ..model_mixins import CrfModelMixin


class Sf12(Sf12ModelMixin, CrfModelMixin, BaseUuidModel):
    class Meta(Sf12ModelMixin.Meta, CrfModelMixin.Meta, BaseUuidModel.Meta):
        pass


# TODO: add proxy model and two options Swahili and English
