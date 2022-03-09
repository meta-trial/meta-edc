from django.db import models
from edc_constants.choices import PRESENT_ABSENT_NA, YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class UrineDipstickTest(CrfModelMixin, edc_models.BaseUuidModel):

    performed = models.CharField(
        verbose_name="Was the urine dipstick test performed?",
        max_length=15,
        choices=YES_NO,
    )

    not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason", max_length=150, null=True, blank=True
    )

    ketones = models.CharField(
        verbose_name="Ketones?",
        max_length=25,
        choices=PRESENT_ABSENT_NA,
        default=NOT_APPLICABLE,
    )

    protein = models.CharField(
        verbose_name="Protein?",
        max_length=25,
        choices=PRESENT_ABSENT_NA,
        default=NOT_APPLICABLE,
    )

    glucose = models.CharField(
        verbose_name="Glucose?",
        max_length=25,
        choices=PRESENT_ABSENT_NA,
        default=NOT_APPLICABLE,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Urine Dipstick Test"
