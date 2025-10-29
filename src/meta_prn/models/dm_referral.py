from clinicedc_constants import NULL_STRING
from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin
from edc_utils.date import get_utcnow

from ..constants import DM_REFFERAL_ACTION


class DmReferral(
    SiteModelMixin,
    ActionModelMixin,
    UniqueSubjectIdentifierFieldMixin,
    BaseUuidModel,
):
    action_name = DM_REFFERAL_ACTION

    report_datetime = models.DateTimeField(
        verbose_name="Report date and time", default=get_utcnow
    )

    referral_date = models.DateField(
        verbose_name="Date of referral to diabetes clinic",
    )

    referral_note = models.TextField(
        verbose_name=(
            "Please provide a brief history of the "
            "diabetes diagnosis that lead to this referral"
        ),
        default=NULL_STRING,
        blank=False,
    )

    class Meta(ActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Diabetes referral"
        verbose_name_plural = "Diabetes referral"
