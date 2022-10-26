from django.db import models
from edc_lab.model_mixins import CrfWithRequisitionModelMixin, requisition_fk_options
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

    requisition = models.ForeignKey(
        limit_choices_to={"panel__name": insulin_panel.name}, **requisition_fk_options
    )

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Blood Result: Insulin"
        verbose_name_plural = "Blood Results: Insulin"
