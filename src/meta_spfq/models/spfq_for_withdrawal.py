from dateutil.relativedelta import relativedelta
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from django.utils import timezone
from django_crypto_fields.fields import EncryptedCharField
from edc_constants.choices import GENDER
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.model_mixins import SiteModelMixin

from .registered_subject_proxy import RegisteredSubjectProxy


class Manager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class SpfqForWithdrawal(UniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):
    registered_subject = models.ForeignKey(
        RegisteredSubjectProxy, on_delete=models.PROTECT, null=True, blank=False
    )

    subject_identifier = models.CharField(max_length=50, null=True, editable=False)  # noqa: DJ001

    report_datetime = models.DateTimeField(blank=True, default=timezone.now)

    upload = models.FileField(upload_to="meta_spfq/")

    initials = EncryptedCharField(null=True, editable=False)
    age_in_years = models.IntegerField(null=True, editable=False)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, editable=False)  # noqa: DJ001

    sid = models.IntegerField(null=True, editable=False, help_text="auto updated")

    objects = Manager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords()

    def __str__(self):
        return str(self.registered_subject)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.registered_subject.subject_identifier
        self.gender = self.registered_subject.gender
        self.initials = self.registered_subject.initials
        self.age_in_years = abs(
            relativedelta(timezone.now().date(), self.registered_subject.dob).years
        )
        self.sid = int(self.registered_subject.sid)
        return super().save(*args, **kwargs)

    def natural_key(self):
        return (self.registered_subject.subject_identifier,)

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "SPFQ for withdrawal transcript"
        verbose_name_plural = "SPFQ for withdrawal transcripts"
