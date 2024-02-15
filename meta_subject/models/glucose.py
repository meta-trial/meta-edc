from django.db import models
from django.utils.translation import gettext as _
from edc_constants.choices import YES_NO
from edc_constants.constants import NO, NOT_APPLICABLE, PENDING, YES
from edc_glucose.model_mixins import (
    fasting_model_mixin_factory,
    fbg_model_mixin_factory,
    ogtt_model_mixin_factory,
)
from edc_model.models import BaseUuidModel
from edc_utils import formatted_date

from ..constants import AMENDMENT_DATE
from ..model_mixins import CrfModelMixin

ENDPOINT_CHOICES = (
    (YES, _(YES)),
    (PENDING, _("No. A repeat FBG will be scheduled")),
    (NO, _(NO)),
    (NOT_APPLICABLE, _("Not applicable")),
)


class Glucose(
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
    ogtt_model_mixin_factory("ogtt"),
    BaseUuidModel,
):
    # TODO: diagnosis of diabetes is OGTT 11.1mmol / L ONLY. Triggers EoS form
    # TODO: move IFG to bloogresultglu. Use this form for OGTT only 27/01/2021

    """A user model to capture IFG and OGTT"""

    fbg_performed = models.CharField(
        verbose_name="Was the FBG test performed?",
        max_length=15,
        choices=YES_NO,
    )

    fbg_not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason", max_length=150, null=True, blank=True
    )

    ogtt_performed = models.CharField(
        verbose_name="Was the OGTT test performed?",
        max_length=15,
        choices=YES_NO,
    )

    ogtt_not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason", max_length=150, null=True, blank=True
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
        verbose_name = "Glucose (IFG, OGTT)"
        verbose_name_plural = "Glucose (IFG, OGTT)"
