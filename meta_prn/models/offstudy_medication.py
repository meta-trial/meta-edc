from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_identifier.model_mixins import (
    NonUniqueSubjectIdentifierFieldMixin,
    TrackingModelMixin,
)
from edc_model import models as edc_models
from edc_model.models import OtherCharField
from edc_sites.models import SiteModelMixin
from edc_utils import get_utcnow

from ..choices import WITHDRAWAL_STUDY_MEDICATION_REASONS
from ..constants import OFFSTUDY_MEDICATION_ACTION


class OffstudyMedication(
    NonUniqueSubjectIdentifierFieldMixin,
    SiteModelMixin,
    ActionModelMixin,
    TrackingModelMixin,
    edc_models.BaseUuidModel,
):

    action_name = OFFSTUDY_MEDICATION_ACTION

    tracking_identifier_prefix = "WM"

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time", default=get_utcnow
    )

    stop_date = models.DateField(
        verbose_name="Date decision to stop study medication",
    )

    last_dose_date = models.DateField(
        verbose_name="Date of last known dose",
    )

    reason = models.CharField(
        verbose_name="Reason for stopping study medication",
        max_length=25,
        choices=WITHDRAWAL_STUDY_MEDICATION_REASONS,
    )

    reason_other = OtherCharField()

    comment = models.TextField(
        verbose_name="Comment",
        null=True,
        blank=True,
    )

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Withdrawal of Study Drug"
        verbose_name_plural = "Withdrawal of Study Drug"
