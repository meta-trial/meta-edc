from edc_blood_results import BLOOD_RESULTS_HBA1C_ACTION
from edc_blood_results.model_mixins import (
    BloodResultsModelMixin,
    Hba1cModelMixin,
    RequisitionModelMixin,
)
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models


class BloodResultsHba1c(
    CrfWithActionModelMixin,
    Hba1cModelMixin,
    RequisitionModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_HBA1C_ACTION
    tracking_identifier_prefix = "HA"

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: HbA1c"
        verbose_name_plural = "Blood Results: HbA1c"
