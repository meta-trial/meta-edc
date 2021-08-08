from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models
from edc_model_fields.fields import OtherCharField

from meta_lists.models import ArvRegimens

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


class OtherArvRegimensDetail(edc_models.BaseUuidModel):

    other_arv_regimens = models.ForeignKey(
        OtherArvRegimens,
        on_delete=models.PROTECT,
    )

    arv_regimen = models.ForeignKey(
        ArvRegimens,
        on_delete=models.PROTECT,
        related_name="other_arv_regimen",
        verbose_name="ARV Regimen",
        null=True,
        blank=False,
    )

    other_arv_regimen = OtherCharField(null=True, blank=True)

    arv_regimen_start_date = models.DateField(
        verbose_name="Start date",
        null=True,
        blank=True,
    )

    notes = models.CharField(
        verbose_name="Notes", max_length=100, null=True, blank=True
    )

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Other ARV Regimens Detail"
        verbose_name_plural = "Other ARV Regimens Detail"
