from edc_model import models as edc_models
from edc_pharmacy.models import StudyMedicationCrfModelMixin

from ..model_mixins import CrfModelMixin


class StudyMedication(StudyMedicationCrfModelMixin, CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(
        StudyMedicationCrfModelMixin.Meta,
        CrfModelMixin.Meta,
        edc_models.BaseUuidModel.Meta,
    ):
        pass
