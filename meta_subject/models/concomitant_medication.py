from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class ConcomitantMedication(CrfModelMixin, BaseUuidModel):

    # prescription
    # days
    # dosage
    # instructions

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Concomitant Medication"
        verbose_name_plural = "Concomitant Medication"
