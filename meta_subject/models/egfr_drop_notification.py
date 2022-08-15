from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_egfr.constants import EGFR_DROP_NOTIFICATION_ACTION
from edc_egfr.model_mixins import EgfrDropNotificationModelMixin
from edc_model import models as edc_models


class EgfrDropNotification(
    EgfrDropNotificationModelMixin,
    CrfWithActionModelMixin,
    edc_models.BaseUuidModel,
):

    action_name = EGFR_DROP_NOTIFICATION_ACTION

    tracking_identifier_prefix = "EG"

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "eGFR Drop Notification"
        verbose_name_plural = "eGFR Drop Notifications"
