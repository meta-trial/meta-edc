from edc_lab.model_mixins import CrfWithRequisitionModelMixin
from edc_lab_panel.panels import lipids_panel
from edc_lab_results import BLOOD_RESULTS_LIPID_ACTION
from edc_lab_results.model_mixins import (
    BloodResultsModelMixin,
    CholModelMixin,
    HdlModelMixin,
    LdlModelMixin,
    TrigModelMixin,
)
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfWithActionModelMixin


class BloodResultsLipid(
    CrfWithActionModelMixin,
    HdlModelMixin,
    LdlModelMixin,
    TrigModelMixin,
    CholModelMixin,
    CrfWithRequisitionModelMixin,
    BloodResultsModelMixin,
    BaseUuidModel,
):
    action_name = BLOOD_RESULTS_LIPID_ACTION
    tracking_identifier_prefix = "LP"
    lab_panel = lipids_panel

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Blood Result: Lipids"
        verbose_name_plural = "Blood Results: Lipids"
