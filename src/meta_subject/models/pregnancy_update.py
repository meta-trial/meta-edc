from django.db import models
from django.db.models import PROTECT
from edc_constants.choices import YES_NO
from edc_model.models import BaseUuidModel
from edc_utils import get_utcnow

from ..model_mixins import CrfModelMixin


class PregnancyUpdate(CrfModelMixin, BaseUuidModel):
    pregnancy_notification = models.ForeignKey(
        "meta_prn.pregnancynotification", on_delete=PROTECT
    )

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time", default=get_utcnow
    )

    contact = models.CharField(
        verbose_name="Has the clinic received any updates on this pregnancy?",
        max_length=15,
        choices=YES_NO,
        help_text="If yes, please specify below",
    )

    comment = models.TextField(verbose_name="Comment / Updates", default="")

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Pregnancy Update"
        verbose_name_plural = "Pregnancy Update"
