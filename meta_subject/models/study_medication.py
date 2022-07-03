from django.core.validators import RegexValidator
from django.db import models
from edc_model import models as edc_models
from edc_model.validators import date_not_future
from edc_pharmacy.models import StudyMedicationCrfModelMixin
from edc_protocol.validators import date_not_before_study_start
from edc_utils import get_utcnow

from ..model_mixins import CrfModelMixin


class StudyMedication(StudyMedicationCrfModelMixin, CrfModelMixin, edc_models.BaseUuidModel):

    roundup_divisible_by = models.IntegerField(default=32)

    # first_dose_date = models.DateField(
    #     verbose_name="Date of first dose",
    #     validators=[date_not_before_study_start, date_not_future],
    #     default=get_utcnow,
    # )
    #
    # sid = models.CharField(
    #     verbose_name="SID# on pill bottles",
    #     max_length=15,
    #     validators=[RegexValidator(regex=r"^\w+$")],
    #     null=True,
    #     blank=False,
    # )

    class Meta(
        StudyMedicationCrfModelMixin.Meta,
        CrfModelMixin.Meta,
        edc_models.BaseUuidModel.Meta,
    ):
        pass
