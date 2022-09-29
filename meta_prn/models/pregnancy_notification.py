from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO, YES_NO_UNSURE
from edc_constants.constants import YES
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_sites.models import SiteModelMixin
from edc_utils import get_utcnow

from meta_subject.models import UrinePregnancy

from ..constants import PREGNANCY_NOTIFICATION_ACTION


class PregnancyNotificationError(Exception):
    pass


class PregnancyNotification(
    SiteModelMixin,
    ActionModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
    BaseUuidModel,
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
        help_text="If YES, the UPT result must already be entered in the EDC.",
    )

    bhcg_date = models.DateField(
        verbose_name="βHCG result date",
        null=True,
        blank=True,
        help_text="Will be validated against a UPT result in the EDC.",
    )

    unconfirmed_details = models.TextField(
        verbose_name="If no, please provide details",
        null=True,
        blank=True,
    )

    edd = models.DateField(
        verbose_name="Estimated date of delivery",
    )

    # TODO: remove this question
    may_contact = models.CharField(
        verbose_name=(
            "Has the participant agreed to be contacted to provide "
            "information on the delivery and birth outcomes?"
        ),
        max_length=15,
        choices=YES_NO_UNSURE,
        help_text=(
            "If YES/UNSURE, a visit will be scheduled on the EDD. "
            "If NO, the participant will be taken off study now"
        ),
        default=YES,
    )

    delivered = models.BooleanField(
        default=False, editable=False, help_text="Auto updated from Delivery"
    )

    delivery_datetime = models.DateTimeField(
        verbose_name="Date and time of delivery :",
        null=True,
        editable=False,
        help_text="Auto updated from Delivery",
    )

    def save(self, *args, **kwargs):
        if (
            not self.id
            and self.bhcg_confirmed == YES
            and not UrinePregnancy.objects.filter(
                subject_visit__subject_identifier=self.subject_identifier,
                notified=False,
                assay_date__lte=self.report_datetime.date(),
            ).exists()
        ):
            raise PregnancyNotificationError(
                "Invalid. A positive Urine βhCG cannot be found. "
                "Perhaps catch this in the form."
            )
        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Pregnancy Notification"
        verbose_name_plural = "Pregnancy Notifications"
        unique_together = ["subject_identifier", "edd"]
