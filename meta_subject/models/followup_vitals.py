from django.db import models
from edc_model import models as edc_models
from edc_vitals.model_mixins import (
    BloodPressureModelMixin,
    SimpleBloodPressureModelMixin,
)

from ..choices import WEIGHT_DETERMINATION
from ..model_mixins import CrfModelMixin, VitalsFieldsModelMixin


class FollowupVitals(
    VitalsFieldsModelMixin,
    BloodPressureModelMixin,
    SimpleBloodPressureModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):

    # TODO: Grading for blood pressure?? sokoine See DAIDS
    # TODO: Add action item modelmixin, grading like blood results

    weight_determination = models.CharField(
        verbose_name="Is weight estimated or measured?",
        max_length=15,
        choices=WEIGHT_DETERMINATION,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Clinic follow up: Vitals"
        verbose_name_plural = "Clinic follow ups: Vitals"
