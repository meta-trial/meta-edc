from django.db import models
from edc_lab.model_mixins import CrfWithRequisitionModelMixin, requisition_fk_options
from edc_lab_panel.panels import hba1c_panel
from edc_lab_results import BLOOD_RESULTS_HBA1C_ACTION
from edc_lab_results.model_mixins import BloodResultsModelMixin, Hba1cModelMixin
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfWithActionModelMixin


class BloodResultsHba1c(
    CrfWithActionModelMixin,
    Hba1cModelMixin,
    CrfWithRequisitionModelMixin,
    BloodResultsModelMixin,
    BaseUuidModel,
):
    action_name = BLOOD_RESULTS_HBA1C_ACTION
    tracking_identifier_prefix = "HA"
    lab_panel = hba1c_panel

    requisition = models.ForeignKey(
        limit_choices_to={"panel__name": hba1c_panel.name}, **requisition_fk_options
    )

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Blood Result: HbA1c"
        verbose_name_plural = "Blood Results: HbA1c"
