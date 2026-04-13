from dateutil.relativedelta import relativedelta
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from django.utils import timezone
from edc_constants.choices import GENDER
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_registration.models import RegisteredSubject
from edc_sites.model_mixins import SiteModelMixin

from meta_rando.models import RandomizationList


class Manager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class SpfqForWithdrawalList(SiteModelMixin, UniqueSubjectIdentifierFieldMixin, BaseUuidModel):
    sid = models.IntegerField(unique=True)

    last_visit_code = models.CharField(max_length=25, null=True)  # noqa: DJ001

    last_appt_datetime = models.DateTimeField(null=True)

    gender = models.CharField(max_length=10, choices=GENDER)

    age_in_years = models.IntegerField()

    objects = Manager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.subject_identifier

    def natural_key(self):
        return (self.subject_identifier,)

    def save(self, *args, **kwargs):
        rs = RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
        self.gender = rs.gender
        self.initials = rs.initials
        self.age_in_years = abs(relativedelta(timezone.now().date(), rs.dob).years)
        rando = RandomizationList.objects.get(subject_identifier=self.subject_identifier)
        self.sid = int(rando.sid)
        return super().save(*args, **kwargs)

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "SPFQ for withdrawal list"
        verbose_name_plural = "SPFQ for withdrawal list"
