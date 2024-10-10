from django.db import models
from edc_model.models import BaseUuidModel
from edc_pharmacy.models import Medication
from edc_randomization.constants import ACTIVE, PLACEBO


class LotNumber(BaseUuidModel):

    lot_no = models.CharField(max_length=25, unique=True)

    medication = models.ForeignKey(
        Medication, on_delete=models.PROTECT, null=True, blank=False
    )

    allocation = models.CharField(
        max_length=25, choices=((ACTIVE, "Active"), (PLACEBO, "Placebo"))
    )

    expiration_date = models.DateField()

    qty = models.IntegerField(null=True)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Lot Number"
        verbose_name_plural = "Lot Numbers"
