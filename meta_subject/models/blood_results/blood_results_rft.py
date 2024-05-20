from django.db import models
from edc_crf.model_mixins import CrfStatusModelMixin
from edc_egfr.model_mixins import EgfrModelMixin
from edc_lab.model_mixins import CrfWithRequisitionModelMixin, requisition_fk_options
from edc_lab_panel.panels import rft_panel
from edc_lab_results import BLOOD_RESULTS_RFT_ACTION
from edc_lab_results.model_mixins import (
    BloodResultsModelMixin,
    CreatinineModelMixin,
    UreaModelMixin,
    UricAcidModelMixin,
)
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfWithActionModelMixin


class BloodResultsRft(
    CrfWithActionModelMixin,
    CreatinineModelMixin,
    EgfrModelMixin,
    UreaModelMixin,
    UricAcidModelMixin,
    CrfWithRequisitionModelMixin,
    BloodResultsModelMixin,
    CrfStatusModelMixin,
    BaseUuidModel,
):
    action_name = BLOOD_RESULTS_RFT_ACTION
    lab_panel = rft_panel
    egfr_formula_name = "ckd-epi"

    requisition = models.ForeignKey(
        limit_choices_to={"panel__name": rft_panel.name}, **requisition_fk_options
    )

    old_egfr_value = models.DecimalField(
        decimal_places=4,
        max_digits=8,
        null=True,
        editable=False,
        help_text="incorrect ckd-epi calculation (w/ 1.150 as ethnicity factor)",
    )

    old_egfr_drop_value = models.DecimalField(
        decimal_places=4,
        max_digits=10,
        null=True,
        editable=False,
        help_text="incorrect ckd-epi calculation (w/ 1.150 as ethnicity factor)",
    )

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Blood Result: RFT"
        verbose_name_plural = "Blood Results: RFT"
