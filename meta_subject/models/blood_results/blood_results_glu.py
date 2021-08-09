from edc_blood_results import BLOOD_RESULTS_GLU_ACTION
from edc_blood_results.model_mixins import (
    BloodResultsModelMixin,
    GlucoseModelMixin,
    RequisitionModelMixin,
)
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models


class BloodResultsGlu(
    CrfWithActionModelMixin,
    GlucoseModelMixin,
    RequisitionModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_GLU_ACTION
    tracking_identifier_prefix = "GL"

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: Glucose"
        verbose_name_plural = "Blood Results: Glucose"
