from edc_blood_results import BLOOD_RESULTS_LIPID_ACTION
from edc_blood_results.model_mixins import (
    BloodResultsModelMixin,
    HdlModelMixin,
    LdlModelMixin,
    RequisitionModelMixin,
    TrigModelMixin,
)
from edc_crf.model_mixins import CrfWithActionModelMixin
from edc_model import models as edc_models


class BloodResultsLipid(
    CrfWithActionModelMixin,
    HdlModelMixin,
    LdlModelMixin,
    TrigModelMixin,
    RequisitionModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_LIPID_ACTION
    tracking_identifier_prefix = "LP"

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: Lipids"
        verbose_name_plural = "Blood Results: Lipids"
