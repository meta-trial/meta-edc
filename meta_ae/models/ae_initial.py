from django.db import models
from edc_adverse_event.model_mixins import AeInitialModelMixin
from edc_model.models import BaseUuidModel


class AeMetaModelMixin(models.Model):
    class Meta:
        abstract = True


class AeInitial(AeInitialModelMixin, AeMetaModelMixin, BaseUuidModel):
    class Meta(AeInitialModelMixin.Meta):
        pass
