from edc_egfr.constants import EGFR_DROP_NOTIFICATION_ACTION
from edc_egfr.model_mixins import EgfrDropNotificationModelMixin
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfWithActionModelMixin


class EgfrDropNotification(
    EgfrDropNotificationModelMixin,
    CrfWithActionModelMixin,
    BaseUuidModel,
):

    action_name = EGFR_DROP_NOTIFICATION_ACTION

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "eGFR Drop Notification"
        verbose_name_plural = "eGFR Drop Notifications"
