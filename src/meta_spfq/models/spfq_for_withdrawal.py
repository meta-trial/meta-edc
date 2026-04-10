from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from edc_constants.choices import GENDER
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.model_mixins import SiteModelMixin


class Manager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class SpfqForWithdrawal(SiteModelMixin, UniqueSubjectIdentifierFieldMixin, BaseUuidModel):
    upload = models.FileField(upload_to="meta_spfq/")
    age_in_years = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER)

    sid = models.IntegerField(null=True, editable=False, help_text="auto updated")
    last_visit_code = models.CharField(  # noqa: DJ001
        max_length=25, null=True, editable=False, help_text="auto updated"
    )
    last_appt_datetime = models.DateTimeField(
        null=True, editable=False, help_text="auto updated"
    )

    objects = Manager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.subject_identifier

    def natural_key(self):
        return (self.subject_identifier,)

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "SPFQ for Withdrawal"
        verbose_name_plural = "SPFQ for Withdrawals"
