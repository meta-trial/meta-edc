from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from edc_constants.choices import GENDER
from edc_constants.constants import NULL_STRING
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.model_mixins import SiteModelMixin


class Manager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class SpfqList(SiteModelMixin, UniqueSubjectIdentifierFieldMixin, BaseUuidModel):
    filename = models.CharField(max_length=100, default=NULL_STRING)

    sid = models.IntegerField(unique=True)

    last_visit_code = models.CharField(max_length=25)

    last_appt_datetime = models.DateTimeField()

    gender = models.CharField(max_length=10, choices=GENDER)

    weight_bin = models.CharField(
        max_length=25,
        choices=(("lt_35", "<35"), ("gte_35__lte_49", "35-49"), ("gte_50", ">=50")),
    )

    age_in_years = models.IntegerField()

    date_generated = models.DateTimeField()

    objects = Manager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.subject_identifier

    def natural_key(self):
        return (self.subject_identifier,)

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "SPFQ List"
        verbose_name_plural = "SPFQ List"
