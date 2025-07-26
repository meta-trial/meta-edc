from edc_mnsi.model_mixins import MnsiModelMixin
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class Mnsi(MnsiModelMixin, CrfModelMixin, BaseUuidModel):
    class Meta(MnsiModelMixin.Meta, CrfModelMixin.Meta, BaseUuidModel.Meta):
        pass
