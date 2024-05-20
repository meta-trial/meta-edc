from django.db import models
from edc_crf.model_mixins import CrfStatusModelMixin, CrfWithActionModelMixin
from edc_lab.model_mixins import CrfWithRequisitionModelMixin, requisition_fk_options
from edc_lab_panel.panels import fbc_panel
from edc_lab_results import BLOOD_RESULTS_FBC_ACTION
from edc_lab_results.model_mixins import (
    BloodResultsModelMixin,
    HaemoglobinModelMixin,
    HctModelMixin,
    MchcModelMixin,
    MchModelMixin,
    McvModelMixin,
    PlateletsModelMixin,
    RbcModelMixin,
    WbcModelMixin,
)
from edc_model.models import BaseUuidModel


class BloodResultsFbc(
    CrfWithActionModelMixin,
    CrfWithRequisitionModelMixin,
    HaemoglobinModelMixin,
    HctModelMixin,
    RbcModelMixin,
    WbcModelMixin,
    PlateletsModelMixin,
    MchModelMixin,
    MchcModelMixin,
    McvModelMixin,
    BloodResultsModelMixin,
    CrfStatusModelMixin,
    BaseUuidModel,
):
    action_name = BLOOD_RESULTS_FBC_ACTION
    tracking_identifier_prefix = "FB"

    lab_panel = fbc_panel

    requisition = models.ForeignKey(
        limit_choices_to={"panel__name": fbc_panel.name}, **requisition_fk_options
    )

    class Meta(CrfWithActionModelMixin.Meta, CrfStatusModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Blood Result: FBC"
        verbose_name_plural = "Blood Results: FBC"
