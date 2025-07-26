from edc_model.models import BaseUuidModel
from edc_transfer.model_mixins import SubjectTransferModelMixin


class SubjectTransfer(
    SubjectTransferModelMixin,
    BaseUuidModel,
):
    class Meta(SubjectTransferModelMixin.Meta, BaseUuidModel.Meta):
        pass
