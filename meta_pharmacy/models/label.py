from django.db import models
from edc_identifier.simple_identifier import SimpleUniqueIdentifier
from edc_model.models import BaseUuidModel

from .lot_number import LotNumber
from .rx import Rx


class LabelIdentifier(SimpleUniqueIdentifier):
    random_string_length = 6
    identifier_type = "rx_label_reference"
    template = "{random_string}"


class Label(BaseUuidModel):

    identifier_cls = LabelIdentifier
    identifier_field_name: str = "rx_label_reference"

    rx = models.ForeignKey(Rx, on_delete=models.PROTECT)
    lot_no = models.ForeignKey(LotNumber, on_delete=models.PROTECT)
    rx_label_reference = models.CharField(max_length=15, unique=True)

    printed_datetime = models.DateTimeField(null=True)
    printed = models.BooleanField(default=False)
    scanned = models.BooleanField(default=False)
    scanned_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return self.rx_label_reference

    def save(self, *args, **kwargs):
        """Label referenceis always allocated."""
        if not self.id:
            setattr(
                self,
                self.identifier_field_name,
                self.identifier_cls().identifier,
            )
        super().save(*args, **kwargs)  # type:ignore

    @property
    def human_readable_identifier(self):
        """Returns a humanized screening identifier."""
        x = self.screening_identifier
        return f"{x[0:4]}-{x[4:]}"

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Label"
        verbose_name_plural = "Labels"
