from django.db import models
from edc_constants.choices import GENDER
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin


class SpfqList(SiteModelMixin, UniqueSubjectIdentifierFieldMixin, BaseUuidModel):
    sid = models.IntegerField(unique=True)

    last_visit_code = models.CharField(max_length=25)

    last_appt_datetime = models.DateTimeField()

    gender = models.CharField(max_length=10, choices=GENDER)

    weight_bin = models.CharField(
        max_length=25,
        choices=(("lt_35", "<35"), ("gte_35__lte_49", "35-49"), ("gte_50", ">=50")),
    )

    date_generated = models.DateTimeField()

    class Meta(BaseUuidModel.Meta):
        verbose_name = "SPFQ List"
        verbose_name_plural = "SPFQ List"
