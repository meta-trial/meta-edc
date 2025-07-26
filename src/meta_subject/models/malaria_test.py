from edc_microscopy.model_mixins import MalariaTestModelMixin
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class MalariaTest(MalariaTestModelMixin, CrfModelMixin, BaseUuidModel):
    class Meta(MalariaTestModelMixin.Meta, CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Malaria Test"
