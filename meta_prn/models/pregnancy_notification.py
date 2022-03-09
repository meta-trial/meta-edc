# TODO: urine_bhcg form (probably not necessary)
# TODO: if pos, take of study drug and estimate delivery date for the pregnancy outcomes form. See Form 25/26
from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import (
    NonUniqueSubjectIdentifierFieldMixin,
    TrackingModelMixin,
)
from edc_model import models as edc_models
from edc_model.models import date_is_future
from edc_sites.models import SiteModelMixin
from edc_utils import get_utcnow

from ..constants import PREGNANCY_NOTIFICATION_ACTION


class PregnancyNotification(
    NonUniqueSubjectIdentifierFieldMixin,
    SiteModelMixin,
    ActionModelMixin,
    TrackingModelMixin,
    edc_models.BaseUuidModel,
):

    action_name = PREGNANCY_NOTIFICATION_ACTION

    tracking_identifier_prefix = "PN"

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time", default=get_utcnow
    )

    bhcg_confirmed = models.CharField(
        verbose_name="Has the pregnancy been confirmed by urine βHCG?",
        max_length=5,
        choices=YES_NO,
    )

    unconfirmed_details = models.TextField(
        verbose_name="If no, please provide details",
        null=True,
        blank=True,
    )

    edd = models.DateField(
        verbose_name="Estimated date of delivery :",
        validators=[date_is_future],
    )

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Pregnancy Notification"
        verbose_name_plural = "Pregnancy Notifications"
        unique_together = ["subject_identifier", "edd"]
