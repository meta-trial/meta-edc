# for reference by old migrations
from edc_lab.managers import RequisitionManager as Manager  # noqa
from edc_lab.model_mixins import RequisitionModelMixin
from edc_model.models import BaseUuidModel
from edc_reference.model_mixins import ReferenceModelMixin


class SubjectRequisition(RequisitionModelMixin, ReferenceModelMixin, BaseUuidModel):
    class Meta(RequisitionModelMixin.Meta, BaseUuidModel.Meta):
        pass
