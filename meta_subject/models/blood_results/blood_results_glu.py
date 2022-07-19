from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_lab.model_mixins import CrfWithRequisitionModelMixin
from edc_lab_panel.panels import blood_glucose_panel
from edc_lab_results import BLOOD_RESULTS_GLU_ACTION
from edc_lab_results.model_mixins import BloodResultsModelMixin, GlucoseModelMixin
from edc_model import models as edc_models


# TODO: this is a IFG!!
class BloodResultsGlu(
    CrfWithActionModelMixin,
    GlucoseModelMixin,
    CrfWithRequisitionModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_GLU_ACTION
    tracking_identifier_prefix = "GL"
    lab_panel = blood_glucose_panel

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: Glucose"
        verbose_name_plural = "Blood Results: Glucose"
