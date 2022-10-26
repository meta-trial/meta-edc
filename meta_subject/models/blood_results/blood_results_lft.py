from django.db import models
from edc_lab.model_mixins import CrfWithRequisitionModelMixin, requisition_fk_options
from edc_lab_panel.panels import lft_panel
from edc_lab_results import BLOOD_RESULTS_LFT_ACTION
from edc_lab_results.model_mixins import (
    AlbuminModelMixin,
    AlpModelMixin,
    AltModelMixin,
    AmylaseModelMixin,
    AstModelMixin,
    BloodResultsModelMixin,
    GgtModelMixin,
)
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfWithActionModelMixin


class BloodResultsLft(
    CrfWithActionModelMixin,
    AlbuminModelMixin,
    AlpModelMixin,
    AltModelMixin,
    AmylaseModelMixin,
    AstModelMixin,
    GgtModelMixin,
    CrfWithRequisitionModelMixin,
    BloodResultsModelMixin,
    BaseUuidModel,
):
    action_name = BLOOD_RESULTS_LFT_ACTION
    tracking_identifier_prefix = "LF"
    lab_panel = lft_panel

    requisition = models.ForeignKey(
        limit_choices_to={"panel__name": lft_panel.name}, **requisition_fk_options
    )

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Blood Result: LFT"
        verbose_name_plural = "Blood Results: LFT"
