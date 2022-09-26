from django.db import models
from edc_model.models import BaseUuidModel
from edc_pharmacy.model_mixins import StudyMedicationCrfModelMixin

from ..model_mixins import CrfModelMixin


class StudyMedication(StudyMedicationCrfModelMixin, CrfModelMixin, BaseUuidModel):

    roundup_divisible_by = models.IntegerField(default=32)

    class Meta(
        StudyMedicationCrfModelMixin.Meta,
        CrfModelMixin.Meta,
        BaseUuidModel.Meta,
    ):
        pass
