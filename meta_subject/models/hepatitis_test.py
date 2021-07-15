from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import POS_NEG_NOT_DONE, YES_NO
from edc_model import models as edc_models

from .model_mixins import CrfModelMixin


class HepatitisTest(CrfModelMixin, edc_models.BaseUuidModel):

    # Hepatitis B Surface Antigen Test
    hbsag_performed = models.CharField(
        verbose_name="Was Hepatitis B Surface Antigen test performed?",
        max_length=15,
        choices=YES_NO,
    )

    hbsag = models.CharField(
        verbose_name=mark_safe("<u>HbSAg</u>"),
        max_length=15,
        choices=POS_NEG_NOT_DONE,
        null=True,
        blank=True,
    )

    hbsag_date = models.DateField(
        verbose_name=mark_safe("<i>HbSAg date</i>"),
        validators=[edc_models.date_is_past, edc_models.date_is_not_now],
        null=True,
        blank=True,
    )

    hcv_performed = models.CharField(
        verbose_name="Was the patient tested for Hepatitis C?",
        max_length=15,
        choices=YES_NO,
    )

    hcv = models.CharField(
        verbose_name=mark_safe("<u>HCV</u>"),
        max_length=15,
        choices=POS_NEG_NOT_DONE,
        null=True,
        blank=True,
    )

    hcv_date = models.DateField(
        verbose_name=mark_safe("<i>HCV date</i>"),
        validators=[edc_models.date_is_past, edc_models.date_is_not_now],
        null=True,
        blank=True,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Hepatitis Tests"
        verbose_name_plural = "Hepatitis Tests"
