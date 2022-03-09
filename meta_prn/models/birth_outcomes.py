from django.db import models
from django.db.models import PROTECT
from edc_action_item.models import ActionModelMixin
from edc_identifier.model_mixins import TrackingModelMixin
from edc_model import models as edc_models
from edc_sites.models import SiteModelMixin
from edc_utils import get_utcnow

from ..choices import FETAL_OUTCOMES
from ..constants import BIRTH_OUTCOME_ACTION
from .delivery import Delivery


class BirthOutcomes(
    SiteModelMixin,
    ActionModelMixin,
    TrackingModelMixin,
    edc_models.BaseUuidModel,
):

    action_name = BIRTH_OUTCOME_ACTION

    tracking_identifier_prefix = "BO"

    delivery = models.ForeignKey(Delivery, on_delete=PROTECT)

    maternal_identifier = models.CharField(max_length=50)

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

    def __str__(self):
        return f"{self.maternal_identifier} #{self.birth_order or '-'}"

    @property
    def subject_identifier(self):
        return self.maternal_identifier

    def save(self, *args, **kwargs):
        self.report_datetime = self.delivery.report_datetime
        self.maternal_identifier = self.delivery.subject_identifier
        super().save(*args, **kwargs)

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Birth Outcomes"
        verbose_name_plural = "Birth Outcomes"
        ordering = ["maternal_identifier", "birth_order"]
        unique_together = ["maternal_identifier", "birth_order"]
