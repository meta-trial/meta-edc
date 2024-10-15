from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_model.models import BaseUuidModel

from .label_batch import LabelBatch


class LabelBatchBarcodes(BaseUuidModel):
    """Inline model for LabelBatch"""

    label_batch = models.ForeignKey(LabelBatch, on_delete=models.PROTECT)

    bottle_count = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)]
    )

    barcodes = models.TextField(blank=True, null=True, help_text="May not exceed 20 barcodes")

    class Meta:
        verbose_name = "Label Batch: Barcodes"
        verbose_name_plural = "Label Batch: Barcodes"
