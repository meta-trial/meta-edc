from django.db import models
from edc_lab.model_mixins import CrfWithRequisitionModelMixin, requisition_fk_options
from edc_lab_panel.panels import blood_glucose_panel
from edc_lab_results import BLOOD_RESULTS_GLU_ACTION
from edc_lab_results.model_mixins import BloodResultsModelMixin, GlucoseModelMixin
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfWithActionModelMixin


# TODO: this is a IFG!!
class BloodResultsGluDummy(
    CrfWithActionModelMixin,
    GlucoseModelMixin,
    CrfWithRequisitionModelMixin,
    BloodResultsModelMixin,
    BaseUuidModel,
):
    action_name = BLOOD_RESULTS_GLU_ACTION
    tracking_identifier_prefix = "GL"
    lab_panel = blood_glucose_panel

    requisition = models.ForeignKey(
        limit_choices_to={"panel__name": blood_glucose_panel.name}, **requisition_fk_options
    )

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Blood Result: Glucose (DUMMY)"
        verbose_name_plural = "Blood Results: Glucose (DUMMY)"
