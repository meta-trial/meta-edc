from django.db import models
from edc_identifier.simple_identifier import SimpleUniqueIdentifier
from edc_model.models import BaseUuidModel
from edc_pharmacy.models import Lot

from .rx import Rx


class LabelIdentifier(SimpleUniqueIdentifier):
    random_string_length = 6
    identifier_type = "rx_label_reference"
    template = "{random_string}"


class RxLabel(BaseUuidModel):
    identifier_cls = LabelIdentifier

    rx = models.ForeignKey(Rx, on_delete=models.PROTECT)
    lot = models.ForeignKey(Lot, on_delete=models.PROTECT)
    label_identifier = models.CharField(max_length=15, unique=True)

    printed_datetime = models.DateTimeField(null=True)
    printed = models.BooleanField(default=False)
    scanned = models.BooleanField(default=False)
    scanned_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return self.label_identifier

    def save(self, *args, **kwargs):
        """Label reference is always allocated."""
        if not self.id:
            self.label_identifier = self.identifier_cls().identifier
        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Label"
        verbose_name_plural = "Labels"
