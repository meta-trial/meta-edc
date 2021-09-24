from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class ConcomitantMedication(CrfModelMixin, edc_models.BaseUuidModel):

    # prescription
    # days
    # dosage
    # instructions

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Concomitant Medication"
        verbose_name_plural = "Concomitant Medication"
