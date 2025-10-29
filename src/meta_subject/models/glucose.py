from clinicedc_constants import NOT_APPLICABLE
from django.db import models
from edc_constants.choices import YES_NO
from edc_glucose.model_mixin_factories import (
    fasting_model_mixin_factory,
    fbg_model_mixin_factory,
    ogtt_model_mixin_factory,
)
from edc_model.models import BaseUuidModel
from edc_utils import formatted_date

from ..choices import ENDPOINT_CHOICES
from ..constants import AMENDMENT_DATE
from ..model_mixins import CrfModelMixin


class Glucose(
    CrfModelMixin,
    fasting_model_mixin_factory(
        None,
        fasting=models.CharField(
            verbose_name="Has the participant fasted?",
            max_length=15,
            choices=YES_NO,
            default="",
            blank=False,
            help_text="As reported by patient",
        ),
    ),
    fbg_model_mixin_factory("fbg"),
    ogtt_model_mixin_factory("ogtt"),
    BaseUuidModel,
):
    """A user model to capture both FBG/RBG and OGTT

    See also GlucoseFbg.
    """

    fbg_performed = models.CharField(
        verbose_name="Was the FBG test performed?",
        max_length=15,
        choices=YES_NO,
    )

    fbg_not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason", max_length=150, default="", blank=True
    )

    ogtt_performed = models.CharField(
        verbose_name="Was the OGTT test performed?",
        max_length=15,
        choices=YES_NO,
    )

    ogtt_not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason", max_length=150, default="", blank=True
    )

    endpoint_today = models.CharField(
        verbose_name="Has the participant reached a study endpoint today?",
        max_length=25,
        choices=ENDPOINT_CHOICES,
        default=NOT_APPLICABLE,
        help_text=(
            f"Response is applicable if reporting after {formatted_date(AMENDMENT_DATE)} "
            "and both the FBG and OGTT were performed"
        ),
    )

    repeat_fbg_date = models.DateField(
        "If required, date particpant to repeat FBG",
        null=True,
        blank=True,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Glucose (FBG/RBG, OGTT)"
        verbose_name_plural = "Glucose (FBG/RBG, OGTT)"
