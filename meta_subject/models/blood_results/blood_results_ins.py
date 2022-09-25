from edc_lab.model_mixins import CrfWithRequisitionModelMixin
from edc_lab_panel.panels import insulin_panel
from edc_lab_results import BLOOD_RESULTS_INSULIN_ACTION
from edc_lab_results.model_mixins import BloodResultsModelMixin, InsulinModelMixin
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfWithActionModelMixin


class BloodResultsIns(
    CrfWithActionModelMixin,
    InsulinModelMixin,
    CrfWithRequisitionModelMixin,
    BloodResultsModelMixin,
    BaseUuidModel,
):
    action_name = BLOOD_RESULTS_INSULIN_ACTION
    tracking_identifier_prefix = "IN"
    lab_panel = insulin_panel

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Blood Result: Insulin"
        verbose_name_plural = "Blood Results: Insulin"
