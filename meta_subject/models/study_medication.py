from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class StudyMedication(CrfModelMixin, edc_models.BaseUuidModel):

    # dosage
    # prescription lasts until (list of study visits, other)
    # special instructions

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Study Medication"
        verbose_name_plural = "Study Medication"
