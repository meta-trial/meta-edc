from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from django.utils import timezone
from edc_crf.model_mixins import CrfStatusModelMixin
from edc_identifier.model_mixins import (
    UniqueSubjectIdentifierFieldMixin,
)
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.model_mixins import SiteModelMixin

from .model_mixins import SpfqRefusalModelMixin


class Manager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class SpfqRefusal(
    UniqueSubjectIdentifierFieldMixin,
    SpfqRefusalModelMixin,
    CrfStatusModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):
    report_datetime = models.DateTimeField(default=timezone.now)

    objects = Manager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.subject_identifier

    def natural_key(self):
        return (self.subject_identifier,)

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "SPFQ Refusal"
        verbose_name_plural = "SPFQ Refusals"
