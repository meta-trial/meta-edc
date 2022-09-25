from django.db import models
from edc_constants.choices import PRESENT_ABSENT_NA, YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel

from ..choices import MALARIA_TEST_CHOICES
from ..model_mixins import CrfModelMixin


class MalariaTest(CrfModelMixin, BaseUuidModel):

    performed = models.CharField(
        verbose_name="Was the malaria test performed?",
        max_length=15,
        choices=YES_NO,
    )

    not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason", max_length=150, null=True, blank=True
    )

    diagnostic_type = models.CharField(
        verbose_name="Diagnostic test used",
        max_length=15,
        choices=MALARIA_TEST_CHOICES,
        default=NOT_APPLICABLE,
    )

    result = models.CharField(
        verbose_name="Result",
        max_length=25,
        choices=PRESENT_ABSENT_NA,
        default=NOT_APPLICABLE,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Malaria Test"
