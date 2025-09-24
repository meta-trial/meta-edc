from django.db import models
from django.db.models import PROTECT, Index
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_crf.model_mixins import CrfStatusModelMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_offstudy.model_mixins import OffstudyCrfModelMixin
from edc_sites.managers import CurrentSiteManager
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow

from ..choices import FETAL_OUTCOMES
from .delivery import Delivery


class Manager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(  # noqa: PLR0913
        self,
        birth_order,
        subject_identifier,
        visit_schedule_name,
        schedule_name,
        visit_code,
        visit_code_sequence,
    ):
        opts = dict(
            birth_order=birth_order,
            delivery__subject_visit__subject_identifier=subject_identifier,
            delivery__subject_visit__visit_schedule_name=visit_schedule_name,
            delivery__subject_visit__schedule_name=schedule_name,
            delivery__subject_visit__visit_code=visit_code,
            delivery__subject_visit__visit_code_sequence=visit_code_sequence,
        )
        return self.get(**opts)


class BirthOutcomes(
    CrfStatusModelMixin,
    SiteModelMixin,
    RequiresConsentFieldsModelMixin,
    OffstudyCrfModelMixin,
    BaseUuidModel,
):
    """A user model to capture birth outcomes.

    Related to the delivery model and presented as an inline
    in Admin.
    """

    delivery = models.ForeignKey(Delivery, on_delete=PROTECT)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=get_utcnow,
    )

    birth_order = models.IntegerField()

    birth_outcome = models.CharField(
        verbose_name="Outcome", max_length=25, choices=FETAL_OUTCOMES
    )

    birth_weight = models.IntegerField(
        verbose_name="Weight (gm)", help_text="gm", null=True, blank=True
    )

    objects = Manager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords(inherit=True)

    def __str__(self):
        return f"{self.delivery} #{self.birth_order or '-'}"

    def natural_key(self) -> tuple:
        return (
            self.birth_order,
            self.delivery.subject_visit.subject_identifier,
            self.delivery.subject_visit.visit_code,
            self.delivery.subject_visit.visit_code_sequence,
            self.delivery.subject_visit.visit_schedule_name,
            self.delivery.subject_visit.visit_schedule,
        )

    def save(self, *args, **kwargs):
        self.report_datetime = self.delivery.report_datetime
        super().save(*args, **kwargs)

    @property
    def related_visit(self):
        return self.delivery.subject_visit

    @property
    def subject_identifier(self):
        return self.delivery.subject_identifier

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Birth Outcomes"
        verbose_name_plural = "Birth Outcomes"
        indexes = (Index(fields=["delivery", "birth_order"]),)
        unique_together = ("delivery", "birth_order")
