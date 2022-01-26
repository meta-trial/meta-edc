from django.db import models
from edc_crf.crf_model_mixin import CrfModelMixin
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models
from edc_visit_tracking.model_mixins import SubjectVisitMissedModelMixin

from meta_lists.models import SubjectVisitMissedReasons
from meta_subject.constants import MISSED_VISIT_ACTION


class SubjectVisitMissed(
    SubjectVisitMissedModelMixin,
    CrfWithActionModelMixin,
    edc_models.BaseUuidModel,
):

    action_name = MISSED_VISIT_ACTION

    tracking_identifier_prefix = "MV"

    action_identifier = models.CharField(max_length=50, unique=True, null=True)

    tracking_identifier = models.CharField(max_length=30, unique=True, null=True)

    missed_reasons = models.ManyToManyField(
        SubjectVisitMissedReasons, blank=True, related_name="meta_missed_reasons"
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Missed Visit Report"
        verbose_name_plural = "Missed Visit Report"
