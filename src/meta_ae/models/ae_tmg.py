from clinicedc_constants import NULL_STRING
from django.db import models
from edc_adverse_event.model_mixins import AeTmgModelMixin
from edc_model.models import BaseUuidModel


class AeTmg(AeTmgModelMixin, BaseUuidModel):
    investigator_ae_classification_comment = models.CharField(
        max_length=250,
        blank=True,
        default=NULL_STRING,
    )

    class Meta(AeTmgModelMixin.Meta):
        verbose_name = "AE TMG Report"
