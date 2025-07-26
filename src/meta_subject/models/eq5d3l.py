from edc_model.models import BaseUuidModel
from edc_qol.model_mixins import Eq5d3lModelMixin

from ..model_mixins import CrfModelMixin


class Eq5d3l(Eq5d3lModelMixin, CrfModelMixin, BaseUuidModel):
    class Meta(Eq5d3lModelMixin.Meta, CrfModelMixin.Meta, BaseUuidModel.Meta):
        pass
