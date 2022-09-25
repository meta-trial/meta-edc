from edc_model.models import BaseUuidModel
from edc_sites.models import CurrentSiteManager
from edc_transfer.model_mixins import SubjectTransferModelMixin


class SubjectTransfer(
    SubjectTransferModelMixin,
    BaseUuidModel,
):

    on_site = CurrentSiteManager()

    class Meta(SubjectTransferModelMixin.Meta, BaseUuidModel.Meta):
        pass
