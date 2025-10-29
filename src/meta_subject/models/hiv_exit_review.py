from clinicedc_constants import NULL_STRING, YES
from django.db import models
from edc_constants.choices import YES_NO
from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_model.models import BaseUuidModel

from meta_lists.models import ArvRegimens

from ..model_mixins import ArvReviewModelMixin, CrfModelMixin


class HivExitReview(SingletonCrfModelMixin, ArvReviewModelMixin, CrfModelMixin, BaseUuidModel):
    available = models.CharField(
        verbose_name="Are HIV test result and treatment information available?",
        max_length=25,
        default=YES,
        choices=YES_NO,
    )

    not_available_reason = models.TextField(
        verbose_name="If not available, please explain ...",
        default=NULL_STRING,
        blank=True,
    )

    current_arv_regimen = models.ForeignKey(
        ArvRegimens,
        on_delete=models.PROTECT,
        related_name="last_arv_regimen",
        verbose_name="Which antiretroviral therapy regimen is the patient currently on?",
        null=True,
        blank=True,
    )

    comment = models.TextField(
        verbose_name="Any other comment?",
        default=NULL_STRING,
        blank=True,
        help_text="May be left blank.",
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "HIV Exit Review"
        verbose_name_plural = "HIV Exit Review"
