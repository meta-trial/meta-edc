from django.db import models
from edc_constants.choices import YES_NO
from edc_glucose.model_mixins import FastingModelMixin, FbgModelMixin, OgttModelMixin
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class Glucose(
    CrfModelMixin,
    FastingModelMixin,
    FbgModelMixin,
    OgttModelMixin,
    edc_models.BaseUuidModel,
):
    # TODO: diagnosis of diabetes is OGTT 11.1mmol / L ONLY. Triggers EoS form
    # TODO: move IFG to bloogresultglu. Use this form for OGTT only 27/01/2021

    """A user model to capture IFG and OGTT"""

    fbg_performed = models.CharField(
        verbose_name="Was the IFG test performed?",
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

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Glucose (IFG, OGTT)"
        verbose_name_plural = "Glucose (IFG, OGTT)"
