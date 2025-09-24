import random

import edc_model.models
from django.db import models
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin

random.seed(237548)


class LabelData(SiteModelMixin, BaseUuidModel):
    subject_identifier = models.CharField(max_length=15, default="")
    sid = models.IntegerField(null=True, help_text="Pharmacy reference")
    reference = models.CharField(
        max_length=10, default="", unique=True, help_text="Bottle reference"
    )
    site_name = models.CharField(max_length=15, default="")
    gender = models.CharField(max_length=5, default="")
    pills_per_bottle = models.IntegerField(null=True, default=128)

    printed_datetime = models.DateTimeField(null=True)
    printed = models.BooleanField(default=False)
    scanned = models.BooleanField(default=False)
    scanned_datetime = models.DateTimeField(null=True)

    received_datetime = models.DateTimeField(null=True)
    received = models.BooleanField(default=False, help_text="Received at site")
    dispensed = models.BooleanField(default=False, help_text="Dispensed to clinic")
    dispensed_datetime = models.DateTimeField(null=True)
    crf = models.BooleanField(default=False, help_text="Entered into subject's CRF")
    crf_datetime = models.DateTimeField(null=True)

    history = edc_model.models.HistoricalRecords()

    class Meta:
        verbose_name = "Label Data"
        verbose_name_plural = "Label Data"
