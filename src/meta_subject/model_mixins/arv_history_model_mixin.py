from django.db import models
from edc_constants.choices import YES_NO
from edc_model.models import OtherCharField

from meta_lists.models import ArvRegimens, OiProphylaxis

from .arv_review_model_mixin import ArvReviewModelMixin


class ArvHistoryModelMixin(ArvReviewModelMixin, models.Model):
    hiv_diagnosis_date = models.DateField(
        verbose_name="When was the diagnosis of HIV made?", null=True, blank=True
    )

    arv_initiation_date = models.DateField(
        verbose_name="Date of start of antiretroviral therapy (ART)",
        null=True,
        blank=True,
    )

    has_previous_arv_regimen = models.CharField(
        verbose_name="Has the patient been on any previous regimen?",
        max_length=15,
        choices=YES_NO,
    )

    previous_arv_regimen = models.ForeignKey(
        ArvRegimens,
        on_delete=models.PROTECT,
        related_name="previous_arv_regimen",
        verbose_name="Which antiretroviral therapy regimen was the patient previously on?",
        null=True,
        blank=True,
    )

    other_previous_arv_regimen = OtherCharField(null=True, blank=True)

    on_oi_prophylaxis = models.CharField(
        verbose_name="Is the patient on any prophylaxis against opportunistic infections?",
        max_length=15,
        choices=YES_NO,
    )

    oi_prophylaxis = models.ManyToManyField(
        OiProphylaxis,
        verbose_name="If YES, which prophylaxis is the patient on?",
        blank=True,
    )

    other_oi_prophylaxis = OtherCharField(null=True, blank=True)

    class Meta:
        abstract = True
