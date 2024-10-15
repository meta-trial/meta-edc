import random
import string

import edc_model.models
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext as _
from edc_constants.constants import CLOSED, OPEN
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin

from .lot_number import LotNumber

random.seed(7685140)

STATUS = (
    (OPEN, _("Open")),
    (CLOSED, _("Closed")),
)


class LabelBatch(SiteModelMixin, BaseUuidModel):

    batch = models.CharField(max_length=15, null=True)

    lot_number = models.ForeignKey(LotNumber, on_delete=models.PROTECT)

    site = models.ForeignKey(Site, on_delete=models.PROTECT)

    # bottle_count = models.IntegerField(null=True, blank=True)
    #
    # barcodes = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=15, choices=STATUS, default=OPEN)

    history = edc_model.models.HistoricalRecords()

    def __str__(self):
        return self.batch

    def save(self, *args, **kwargs):
        if not self.id:
            batch = "".join(  # nosec B311
                random.choices(string.ascii_letters.upper() + "0123456789", k=6)  # nosec B311
            )  # nosec B311
            self.batch = f"{self.site.id}{batch}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Label Batch"
        verbose_name_plural = "Label Batch"
