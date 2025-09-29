from django.conf import settings
from django.db import models
from edc_model.models import BaseUuidModel
from edc_transfer.model_mixins import SubjectTransferModelMixin


class SubjectTransfer(
    SubjectTransferModelMixin,
    BaseUuidModel,
):
    transfer_reason = models.ManyToManyField(
        f"{settings.LIST_MODEL_APP_LABEL}.transferreasons",
        verbose_name="Reason for transfer",
    )

    class Meta(SubjectTransferModelMixin.Meta, BaseUuidModel.Meta):
        pass
