# for reference by old migrations
from edc_lab.managers import RequisitionManager as Manager  # noqa
from edc_lab.model_mixins import RequisitionModelMixin
from edc_model import models as edc_models
from edc_reference.model_mixins import ReferenceModelMixin


class SubjectRequisition(RequisitionModelMixin, ReferenceModelMixin, edc_models.BaseUuidModel):
    class Meta(RequisitionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        pass
