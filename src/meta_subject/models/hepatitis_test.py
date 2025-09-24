from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import POS_NEG, YES_NO
from edc_model.models import BaseUuidModel
from edc_model.validators import date_is_not_now, date_is_past

from ..model_mixins import CrfModelMixin


class HepatitisTest(CrfModelMixin, BaseUuidModel):
    # Hepatitis B Surface Antigen Test
    hbsag_performed = models.CharField(
        verbose_name="Was Hepatitis B Surface Antigen test performed?",
        max_length=15,
        choices=YES_NO,
        help_text="Answer `YES` if `ever` performed and a result is available.",
    )

    hbsag = models.CharField(
        verbose_name=mark_safe("<u>HbSAg</u>"),  # nosec B308
        max_length=15,
        choices=POS_NEG,
        default="",
        blank=True,
    )

    hbsag_date = models.DateField(
        verbose_name=mark_safe("<i>HbSAg date</i>"),  # nosec B308
        validators=[date_is_past, date_is_not_now],
        null=True,
        blank=True,
        help_text="Approximate if not known",
    )

    hcv_performed = models.CharField(
        verbose_name="Was the patient tested for Hepatitis C?",
        max_length=15,
        choices=YES_NO,
        help_text="Answer `YES` if `ever` performed and a result is available.",
    )

    hcv = models.CharField(
        verbose_name=mark_safe("<u>HCV</u>"),  # nosec B308
        max_length=15,
        choices=POS_NEG,
        default="",
        blank=True,
    )

    hcv_date = models.DateField(
        verbose_name=mark_safe("<i>HCV date</i>"),  # nosec B308
        validators=[date_is_past, date_is_not_now],
        null=True,
        blank=True,
        help_text="Approximate if not known",
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Hepatitis Tests"
        verbose_name_plural = "Hepatitis Tests"
