from clinicedc_constants import NULL_STRING
from django.db import models
from edc_adverse_event.model_mixins import AeInitialModelMixin
from edc_model.models import BaseUuidModel

from meta_ae.pdf_reports import AePdfReport


class AeMetaModelMixin(models.Model):
    class Meta:
        abstract = True


class AeInitial(AeInitialModelMixin, AeMetaModelMixin, BaseUuidModel):
    pdf_report_cls = AePdfReport

    ae_classification_comment = models.CharField(
        max_length=250,
        blank=True,
        default=NULL_STRING,
    )

    class Meta(AeInitialModelMixin.Meta):
        pass
