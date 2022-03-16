from django.db import models
from django.db.models import PROTECT
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models
from edc_utils import get_utcnow

from ..choices import FETAL_OUTCOMES
from .delivery import Delivery


class BirthOutcomes(
    CrfWithActionModelMixin,
    edc_models.BaseUuidModel,
):

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

    def __str__(self):
        return f"{self.subject_identifier} #{self.birth_order or '-'}"

    def save(self, *args, **kwargs):
        self.report_datetime = self.delivery.report_datetime
        self.subject_visit = self.delivery.subject_visit
        super().save(*args, **kwargs)

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Birth Outcomes"
        verbose_name_plural = "Birth Outcomes"
        ordering = ["delivery", "birth_order"]
        unique_together = ["delivery", "birth_order"]
