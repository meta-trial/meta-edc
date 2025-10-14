from django.db import models
from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_model.models import BaseUuidModel

from meta_lists.models import ArvRegimens

from ..model_mixins import ArvReviewModelMixin, CrfModelMixin


class HivExitReview(SingletonCrfModelMixin, ArvReviewModelMixin, CrfModelMixin, BaseUuidModel):
    current_arv_regimen = models.ForeignKey(
        ArvRegimens,
        on_delete=models.PROTECT,
        related_name="last_arv_regimen",
        verbose_name="Which antiretroviral therapy regimen is the patient currently on?",
        null=True,
        blank=False,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "HIV Exit Review"
        verbose_name_plural = "HIV Exit Review"
