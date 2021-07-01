from edc_blood_results import BLOOD_RESULTS_RFT_ACTION
from edc_blood_results.model_mixins import (
    BloodResultsModelMixin,
    CreatinineModelMixin,
    EgfrModelMixin,
    RequisitionModelMixin,
    UreaModelMixin,
    UricModelMixin,
)
from edc_crf.model_mixins import CrfWithActionModelMixin
from edc_model import models as edc_models


class BloodResultsRft(
    CrfWithActionModelMixin,
    CreatinineModelMixin,
    EgfrModelMixin,
    UreaModelMixin,
    UricModelMixin,
    RequisitionModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_RFT_ACTION
    tracking_identifier_prefix = "RF"

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: RFT"
        verbose_name_plural = "Blood Results: RFT"
