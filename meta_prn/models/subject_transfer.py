from edc_model import models as edc_models
from edc_sites.models import CurrentSiteManager
from edc_transfer.model_mixins import SubjectTransferModelMixin


class SubjectTransfer(
    SubjectTransferModelMixin,
    edc_models.BaseUuidModel,
):

    on_site = CurrentSiteManager()

    class Meta(SubjectTransferModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        pass
