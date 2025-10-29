from clinicedc_constants import QUESTION_RETIRED
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_RETIRED
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField

from ...model_mixins import CrfModelMixin


class DmEndpoint(CrfModelMixin, BaseUuidModel):
    """A user model to enrolled patient onto the DM Referral
    Schedule.
    """

    endpoint_reached = models.CharField(
        verbose_name="Was the patient referred because the diabetes endpoint was reached?",
        max_length=15,
        choices=YES_NO,
        default="",
        blank=False,
        help_text="If YES, the EDC will check for the patient on the Endpoints report.",
    )

    # retired
    dx_date = models.DateField(verbose_name="Date endpoint reached", null=True)

    # retired
    dx_initiated_by = models.CharField(
        verbose_name="What initiated the diagnosis",
        max_length=25,
        default=QUESTION_RETIRED,
    )

    # retired
    dx_initiated_by_other = OtherCharField(blank=True)

    # retired
    dx_tmg = models.CharField(
        verbose_name="Was this case discussed with the TMG?",
        max_length=25,
        choices=YES_NO_RETIRED,
        default=QUESTION_RETIRED,
    )

    # retired
    dx_tmg_date = models.DateField(
        verbose_name="If YES, provide the date of the TMG discussion", null=True, blank=True
    )

    # retired
    dx_no_tmg_reason = models.TextField(
        verbose_name="If NO, please explain why this case was not discussed with the TMG",
        default="",
        blank=True,
    )

    comments = models.TextField(verbose_name="Any other comments", default="", blank=True)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Diabetes endpoint"
        verbose_name_plural = "Diabetes endpoint"
