from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import POS_NEG, YES_NO
from edc_model import models as edc_models

from ..constants import URINE_PREGNANCY_ACTION
from ..model_mixins import CrfModelMixin
from ..model_mixins.crf_model_mixin import CrfWithActionModelMixin


class UrinePregnancy(CrfWithActionModelMixin, edc_models.BaseUuidModel):

    action_name = URINE_PREGNANCY_ACTION
    tracking_identifier_prefix = "UP"

    performed = models.CharField(
        verbose_name="Was the urine pregnancy test performed?",
        max_length=15,
        choices=YES_NO,
    )

    not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason", max_length=150, null=True, blank=True
    )

    assay_date = models.DateTimeField(
        verbose_name="Urine βhCG date", blank=True, null=True
    )

    bhcg_value = models.CharField(
        verbose_name="Urine βhCG result",
        max_length=25,
        choices=POS_NEG,
    )

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Urine Pregnancy"
