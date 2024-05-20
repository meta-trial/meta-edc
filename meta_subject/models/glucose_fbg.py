from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_glucose.model_mixins import (
    fasting_model_mixin_factory,
    fbg_model_mixin_factory,
)
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class GlucoseFbg(
    CrfModelMixin,
    fasting_model_mixin_factory(
        None,
        fasting=models.CharField(
            verbose_name="Has the participant fasted?",
            max_length=15,
            choices=YES_NO,
            null=True,
            blank=False,
            help_text="As reported by patient",
        ),
    ),
    fbg_model_mixin_factory("fbg"),
    BaseUuidModel,
):

    fbg_performed = models.CharField(
        verbose_name="Was the FBG test performed?",
        max_length=15,
        choices=YES_NO,
    )

    fbg_not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason",
        max_length=150,
        null=True,
        blank=True,
    )

    fasting_duration_estimated = models.CharField(
        max_length=15,
        default=NO,
        editable=False,
        help_text=(
            "Set to YES for existing values before duration "
            "question was added to the form, otherwise NO"
        ),
    )

    repeat_fbg_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date should be within 1 week of report date",
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Glucose (FBG)"
        verbose_name_plural = "Glucose (FBG)"
