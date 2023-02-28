from django.db import models
from edc_model.models import BaseUuidModel
from edc_visit_tracking.model_mixins import SubjectVisitMissedModelMixin

from meta_lists.models import SubjectVisitMissedReasons

from ..constants import MISSED_VISIT_ACTION
from ..model_mixins import CrfWithActionModelMixin


class SubjectVisitMissed(
    SubjectVisitMissedModelMixin,
    CrfWithActionModelMixin,
    BaseUuidModel,
):
    action_name = MISSED_VISIT_ACTION

    missed_reasons = models.ManyToManyField(
        SubjectVisitMissedReasons, blank=True, related_name="meta_missed_reasons"
    )

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Missed Visit Report"
        verbose_name_plural = "Missed Visit Report"
