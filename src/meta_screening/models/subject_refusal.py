from django.db import models
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_model.models import BaseUuidModel
from edc_model.models.historical_records import HistoricalRecords
from edc_model_fields.fields.other_charfield import OtherCharField
from edc_search.model_mixins import SearchSlugManager
from edc_sites.managers import CurrentSiteManager
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow

from ..choices import REFUSAL_REASONS
from .subject_screening import SubjectScreening


class SubjectRefusalManager(SearchSlugManager, models.Manager):
    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class SubjectRefusal(NonUniqueSubjectIdentifierModelMixin, SiteModelMixin, BaseUuidModel):
    subject_screening = models.ForeignKey(SubjectScreening, on_delete=models.PROTECT)

    subject_identifier = models.CharField(max_length=50, editable=False)

    screening_identifier = models.CharField(max_length=50, editable=False)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time", default=get_utcnow
    )

    reason = models.CharField(
        verbose_name="Reason for refusal to join",
        max_length=25,
        choices=REFUSAL_REASONS,
    )

    other_reason = OtherCharField()

    objects = SubjectRefusalManager()

    on_site = CurrentSiteManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.screening_identifier = self.subject_screening.screening_identifier
        self.subject_identifier = self.subject_screening.subject_identifier
        self.subject_identifier_as_pk = self.subject_screening.subject_identifier_as_pk
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.screening_identifier} {self.subject_screening.gender} "
            f"{self.subject_screening.age_in_years}"
        )

    def natural_key(self):
        return (self.subject_identifier,)

    def get_search_slug_fields(self):
        return "screening_identifier", "subject_identifier"

    class Meta:
        verbose_name = "Subject Refusal"
        verbose_name_plural = "Subject Refusals"
