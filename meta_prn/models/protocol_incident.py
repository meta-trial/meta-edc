from django.db import models
from edc_action_item.models import ActionItem, ActionModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_protocol_incident.constants import PROTOCOL_INCIDENT_ACTION
from edc_protocol_incident.model_mixins import ProtocolIncidentModelMixin
from edc_sites.models import SiteModelMixin

from ..choices import ACTION_REQUIRED


class ProtocolIncident(
    SiteModelMixin,
    ActionModelMixin,
    ProtocolIncidentModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
    BaseUuidModel,
):

    action_name = PROTOCOL_INCIDENT_ACTION

    action_item = models.ForeignKey(
        ActionItem,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="meta_prn_action_item",
    )

    action_required_old = models.CharField(max_length=45, choices=ACTION_REQUIRED, null=True)

    def natural_key(self):
        return (self.action_identifier,)  # noqa

    class Meta(ProtocolIncidentModelMixin.Meta, BaseUuidModel.Meta):
        pass
