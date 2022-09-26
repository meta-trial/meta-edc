from django.db import models
from edc_crf.model_mixins import CrfInlineModelMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model.validators import date_is_not_now, date_not_future
from edc_model_fields.fields import OtherCharField
from edc_sites.models import CurrentSiteManager

from meta_lists.models import ArvRegimens

from .other_arv_regimens import OtherArvRegimens


class InlineModelManager(models.Manager):

    use_in_migrations = True

    def get_by_natural_key(
        self,
        other_arv_regimens,
        arv_regimen,
    ):
        return self.get(other_arv_regimens=other_arv_regimens, arv_regimen=arv_regimen)


class OtherArvRegimensDetail(CrfInlineModelMixin, BaseUuidModel):

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
        validators=[date_not_future, date_is_not_now],
        null=True,
        blank=True,
    )

    notes = models.CharField(verbose_name="Notes", max_length=100, null=True, blank=True)

    on_site = CurrentSiteManager()
    objects = InlineModelManager()
    history = HistoricalRecords(inherit=True)

    def natural_key(self) -> tuple:
        return self.other_arv_regimens, self.arv_regimen

    class Meta(CrfInlineModelMixin.Meta, BaseUuidModel.Meta):
        crf_inline_parent = "other_arv_regimens"
        verbose_name = "Other ARV Regimens Detail"
        verbose_name_plural = "Other ARV Regimens Detail"
