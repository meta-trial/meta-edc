from django.core.validators import MinValueValidator
from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import ALIVE_DEAD_UNKNOWN, YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_crf.model_mixins import CrfModelMixin
from edc_identifier.model_mixins import TrackingModelMixin
from edc_model import models as edc_models
from edc_model.validators import date_not_future
from edc_protocol.validators import date_not_before_study_start
from edc_utils import get_utcnow
from meta_lists.models import MissedVisitReasons


class MissedVisit(
    CrfModelMixin,
    SubjectVisitMissedModelMixin,
    ActionModelMixin,
    TrackingModelMixin,
    edc_models.BaseUuidModel,
):

    action_name = SUBJECT_MISSED_VISIT_ACTION

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Missed Visit Report"
        verbose_name_plural = "Missed Visit Report"
