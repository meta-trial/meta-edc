from django.db import models
from edc_constants.choices import YES_NO
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..model_mixins import CrfModelMixin


class OffStudyMedication(CrfModelMixin, BaseUuidModel):

    last_dose_date = models.DateField(
        verbose_name="Date of last known dose",
        validators=[date_not_before_study_start, date_not_future],
    )

    last_dose_date_estimated = models.CharField(
        verbose_name="Is this date estimated",
        max_length=15,
        choices=YES_NO,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        pass
