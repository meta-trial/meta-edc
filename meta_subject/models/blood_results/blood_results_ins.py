from edc_blood_results import BLOOD_RESULTS_INSULIN_ACTION
from edc_blood_results.model_mixins import (
    BloodResultsModelMixin,
    InsulinModelMixin,
    RequisitionModelMixin,
)
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_lab_panel.panels import insulin_panel
from edc_model import models as edc_models


class BloodResultsIns(
    CrfWithActionModelMixin,
    InsulinModelMixin,
    RequisitionModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_INSULIN_ACTION
    tracking_identifier_prefix = "IN"
    lab_panel = insulin_panel

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: Insulin"
        verbose_name_plural = "Blood Results: Insulin"
