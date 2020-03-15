from django.db import models
from edc_action_item.models.action_model_mixin import ActionModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import OTHER
from edc_identifier.model_mixins import (
    TrackingModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
)
from edc_model.models.base_uuid_model import BaseUuidModel
from edc_sites.models import SiteModelMixin
from edc_utils.date import get_utcnow

from ..constants import LOSS_TO_FOLLOWUP_ACTION


LOSS_CHOICES = (
    ("unknown_address", "Changed to an unknown address"),
    ("never_returned", "Did not return despite reminders"),
    ("bad_contact_details", "Inaccurate contact details"),
    (OTHER, "Other"),
)


class LossToFollowup(
    NonUniqueSubjectIdentifierFieldMixin,
    SiteModelMixin,
    ActionModelMixin,
    TrackingModelMixin,
    BaseUuidModel,
):

    action_name = LOSS_TO_FOLLOWUP_ACTION

    tracking_identifier_prefix = "LF"

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time", default=get_utcnow
    )

    last_seen_datetime = models.DateField(verbose_name="Date participant last seen")

    phone_attempts = models.IntegerField(
        verbose_name=(
            "How many attempts have been made to contact the participant by phone"
        )
    )

    home_visited = models.CharField(
        verbose_name="Has a home visit been made", max_length=15, choices=YES_NO
    )

    home_visit_detail = models.TextField(
        verbose_name="If YES, provide any further details of the home visit",
        null=True,
        blank=False,
    )

    loss_category = models.CharField(
        verbose_name="Category of loss to follow up", max_length=25, choices=""
    )

    comment = models.TextField(
        verbose_name=(
            "Please give details of the circumstances that have led to this decision."
        ),
        null=True,
        blank=False,
    )

    class Meta:
        verbose_name = "Loss to Follow Up"
        verbose_name = "Loss to Follow Ups"
        indexes = [
            models.Index(
                fields=["subject_identifier", "action_identifier", "site", "id"]
            )
        ]
