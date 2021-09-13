from django.db import models
from edc_action_item.models import ActionItem, ActionModelMixin
from edc_constants.choices import NOT_APPLICABLE
from edc_identifier.model_mixins import (
    NonUniqueSubjectIdentifierFieldMixin,
    TrackingModelMixin,
)
from edc_model.models import BaseUuidModel
from edc_protocol_violation.constants import PROTOCOL_DEVIATION_VIOLATION_ACTION
from edc_protocol_violation.model_mixins import ProtocolDeviationViolationModelMixin
from edc_sites.models import SiteModelMixin

from ..choices import ACTION_REQUIRED, PROTOCOL_VIOLATION


class ProtocolDeviationViolation(
    ProtocolDeviationViolationModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
    SiteModelMixin,
    ActionModelMixin,
    TrackingModelMixin,
    BaseUuidModel,
):

    action_name = PROTOCOL_DEVIATION_VIOLATION_ACTION

    action_item = models.ForeignKey(
        ActionItem,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="meta_prn_action_item",
    )

    violation_type = models.CharField(
        verbose_name="Type of violation",
        max_length=75,
        choices=PROTOCOL_VIOLATION,
        default=NOT_APPLICABLE,
    )

    violation_type_other = models.CharField(
        null=True, blank=True, verbose_name="If other, please specify", max_length=75
    )

    action_required_old = models.CharField(
        max_length=45, choices=ACTION_REQUIRED, null=True
    )

    def natural_key(self):
        return (self.action_identifier,)

    class Meta(ProtocolDeviationViolationModelMixin.Meta, BaseUuidModel.Meta):
        pass
