from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import OTHER
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField

from ...model_mixins import CrfModelMixin

DM_DX_CHOICES = (
    ("fbg_confirmed", "Any FBG >= 7.0 mmol/L (confirmed by OGTT)"),
    ("fbg_unconfirmed", "Any FBG >= 7.0 mmol/L (NOT confirmed by OGTT)"),
    ("ogtt_annaul", "Annual OGTT >= 11.1 mmol/L"),
    ("ogtt_unscheduled", "Any OGTT >= 11.1 mmol/L (excluding annual or used in confirmation)"),
    (OTHER, "Other"),
)


class DmDiagnosis(CrfModelMixin, BaseUuidModel):

    dx_date = models.DateField(verbose_name="Date of diagnosis")

    dx_initiated_by = models.CharField(
        verbose_name="What initiated the diagnosis",
        max_length=25,
        choices=DM_DX_CHOICES,
    )

    dx_initiated_by_other = OtherCharField()

    dx_tmg = models.CharField(
        verbose_name="Was this case discussed with the TMG?",
        max_length=15,
        choices=YES_NO,
    )

    dx_tmg_date = models.DateField(
        verbose_name="If YES, provide the date of the TMG discussion", null=True, blank=True
    )

    dx_no_tmg_reason = models.TextField(
        verbose_name="If NO, please explain why this case was not discussed with the TMG",
        null=True,
        blank=True,
    )

    comments = models.TextField(verbose_name="Any other comments", null=True, blank=True)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Diabetes diagnosis"
        verbose_name_plural = "Diabetes diagnosis"
