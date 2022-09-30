from django.db import models
from edc_action_item.models.action_model_mixin import ActionModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import OTHER
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_ltfu.constants import LTFU_ACTION
from edc_model.models import BaseUuidModel, OtherCharField
from edc_sites.models import SiteModelMixin
from edc_utils.date import get_utcnow

LOSS_CHOICES = (
    ("unknown_address", "Changed to an unknown address"),
    ("never_returned", "Did not return despite reminders"),
    ("bad_contact_details", "Inaccurate contact details"),
    (OTHER, "Other, please specify ..."),
)


class LossToFollowup(
    SiteModelMixin,
    ActionModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
    BaseUuidModel,
):

    action_name = LTFU_ACTION

    tracking_identifier_prefix = "LF"

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time", default=get_utcnow
    )

    last_seen_datetime = models.DateField(verbose_name="Date participant last seen")

    number_consecutive_missed_visits = models.DateField(
        verbose_name="Number of consecutive visits missed", null=True, blank=False
    )

    # TODO has the patient been off study medication for more than 6 months. If no, not LTFU!!

    last_missed_visit_datetime = models.DateField(
        verbose_name="Date of last missed visit report submitted",
        null=True,
        blank=False,
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
        verbose_name="Category of loss to follow up",
        max_length=25,
        choices=LOSS_CHOICES,
    )

    loss_category_other = OtherCharField()

    comment = models.TextField(
        verbose_name=(
            "Please give details of the circumstances that have led to this decision."
        ),
        null=True,
        blank=False,
    )

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Loss to Follow Up"
        verbose_name_plural = "Loss to Follow Up"
        indexes = [
            models.Index(fields=["subject_identifier", "action_identifier", "site", "id"])
        ]
