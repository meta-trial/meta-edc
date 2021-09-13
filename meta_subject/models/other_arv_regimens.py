from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class OtherArvRegimens(CrfModelMixin, edc_models.BaseUuidModel):
    has_other_regimens = models.CharField(
        verbose_name=(
            "Are there additional ARV regimens to report "
            "NOT reported on the Patient History CRF?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Other ARV Regimens"
        verbose_name_plural = "Other ARV Regimens"
