from edc_adherence.model_mixins import MedicationAdherenceModelMixin
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class MedicationAdherence(MedicationAdherenceModelMixin, CrfModelMixin, BaseUuidModel):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Medication Adherence"
        verbose_name_plural = "Medication Adherence"
