from django.db import models
from edc_constants.constants import COMPLETE, INCOMPLETE, NEW, OPEN
from edc_crf.crf_status_model_mixin import CrfStatusModelMixin
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models
from edc_utils import get_utcnow

from meta_screening.models.creatinine_fields_model_mixin import (
    CreatinineModelFieldsMixin,
)

from ..choices import REPORT_STATUS
from ..constants import EGFR_DROP_NOTIFICATION_ACTION


class EgfrDropNotification(
    CrfStatusModelMixin,
    CrfWithActionModelMixin,
    CreatinineModelFieldsMixin,
    edc_models.BaseUuidModel,
):

    action_name = EGFR_DROP_NOTIFICATION_ACTION

    tracking_identifier_prefix = "EG"

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time", default=get_utcnow
    )

    creatinine_date = models.DateField(verbose_name="Creatinine result date")

    egfr_percent_change = models.DecimalField(
        verbose_name="Change from baseline",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Copied from RFT result eGFR section",
    )

    narrative = models.TextField(
        verbose_name="Narrative",
        null=True,
        blank=True,
    )

    report_status = models.CharField(max_length=15, choices=REPORT_STATUS, default=NEW)

    def save(self, *args, **kwargs):
        if self.report_status == OPEN:
            self.crf_status = INCOMPLETE
        else:
            self.crf_status = COMPLETE
        super().save(*args, **kwargs)

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "eGFR Drop Notification"
        verbose_name_plural = "eGFR Drop Notifications"
