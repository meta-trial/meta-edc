from edc_blood_results import BLOOD_RESULTS_RFT_ACTION
from edc_blood_results.model_mixins import (
    BloodResultsModelMixin,
    CreatinineModelMixin,
    EgfrModelMixin,
    RequisitionModelMixin,
    UreaModelMixin,
    UricAcidModelMixin,
)
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_lab_panel.panels import rft_panel
from edc_model import models as edc_models
from edc_reportable import calculate_egfr
from edc_reportable.units import EGFR_UNITS
from edc_screening.utils import get_subject_screening_model_cls


class BloodResultsRft(
    CrfWithActionModelMixin,
    CreatinineModelMixin,
    EgfrModelMixin,
    UreaModelMixin,
    UricAcidModelMixin,
    RequisitionModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_RFT_ACTION
    tracking_identifier_prefix = "RF"
    lab_panel = rft_panel

    def save(self, *args, **kwargs):
        if self.creatinine_value:
            subject_screening = get_subject_screening_model_cls().objects.get(
                subject_identifier=self.subject_visit.subject_identifier
            )
            self.egfr_value = calculate_egfr(
                gender=subject_screening.gender,
                ethnicity=subject_screening.ethnicity,
                age_in_years=subject_screening.age_in_years,
                creatinine_value=self.creatinine_value,
                creatinine_units=self.creatinine_units,
            )
            self.egfr_units = EGFR_UNITS
        super().save(*args, **kwargs)

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: RFT"
        verbose_name_plural = "Blood Results: RFT"
