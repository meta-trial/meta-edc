from django.db import models
from edc_clinic.models import (
    FastingModelMixin,
    OgttModelMixin,
    FastingGlucoseModelMixin,
)
from edc_constants.choices import YES_NO
from edc_crf.model_mixins import CrfModelMixin
from edc_model import models as edc_models


class Glucose(
    CrfModelMixin,
    FastingModelMixin,
    FastingGlucoseModelMixin,
    OgttModelMixin,
    edc_models.BaseUuidModel,
):

    ifg_performed = models.CharField(
        verbose_name="Was the IFG test performed?", max_length=15, choices=YES_NO,
    )

    ifg_not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason", max_length=150, null=True, blank=True
    )

    ogtt_performed = models.CharField(
        verbose_name="Was the OGTT test performed?", max_length=15, choices=YES_NO,
    )

    ogtt_not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason", max_length=150, null=True, blank=True
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Glucose (IFG, OGTT)"
        verbose_name_plural = "Glucose (IFG, OGTT)"
