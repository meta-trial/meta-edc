from clinicedc_constants import NOT_APPLICABLE, NULL_STRING
from django.contrib.sites.managers import CurrentSiteManager
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_crf.model_mixins import CrfStatusModelMixin
from edc_identifier.model_mixins import (
    UniqueSubjectIdentifierFieldMixin,
)
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.model_mixins import SiteModelMixin


class Manager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class SpfqRefusal(
    UniqueSubjectIdentifierFieldMixin, CrfStatusModelMixin, SiteModelMixin, BaseUuidModel
):
    report_datetime = models.DateTimeField(default=timezone.now)

    contact_attempted = models.CharField(
        verbose_name=_("Were any attempts made to contact the participant?"),
        max_length=25,
        choices=YES_NO,
    )

    contact_attempts_count = models.IntegerField(
        verbose_name=_("Number of attempts made to contact participant"),
        validators=[MinValueValidator(1)],
        help_text=_("Multiple attempts on the same day count as a single attempt."),
        null=True,
        blank=True,
    )

    contact_made = models.CharField(
        verbose_name=_("Was contact made with the participant?"),
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    contact_attempts_explained = models.TextField(
        verbose_name=_("If contact not made and less than 3 attempts, please explain"),
        default=NULL_STRING,
        blank=True,
    )

    reason = models.TextField(
        verbose_name="Why is this participant not consenting to the sub-study?",
        default=NULL_STRING,
    )

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
