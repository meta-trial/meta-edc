from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from edc_constants.constants import CLOSED, NEW, OPEN
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_lab.model_mixins import CrfWithRequisitionModelMixin
from edc_lab_panel.panels import rft_panel
from edc_lab_results import BLOOD_RESULTS_RFT_ACTION
from edc_lab_results.model_mixins import (
    BloodResultsModelMixin,
    CreatinineModelMixin,
    EgfrModelMixin,
    UreaModelMixin,
    UricAcidModelMixin,
)
from edc_model import models as edc_models
from edc_reportable import EgfrCkdEpi
from edc_reportable.calculators import egfr_percent_change
from edc_reportable.units import EGFR_UNITS
from edc_screening.utils import get_subject_screening_model_cls
from edc_visit_schedule.constants import DAY1
from edc_visit_schedule.utils import is_baseline


class BloodResultsRft(
    CrfWithActionModelMixin,
    CreatinineModelMixin,
    EgfrModelMixin,
    UreaModelMixin,
    UricAcidModelMixin,
    CrfWithRequisitionModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    action_name = BLOOD_RESULTS_RFT_ACTION
    tracking_identifier_prefix = "RF"
    lab_panel = rft_panel

    egfr_percent_change = models.DecimalField(
        verbose_name="Percent change from baseline",
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.creatinine_value:
            subject_screening = get_subject_screening_model_cls().objects.get(
                subject_identifier=self.subject_visit.subject_identifier
            )
            self.egfr_value = EgfrCkdEpi(
                gender=subject_screening.gender,
                ethnicity=subject_screening.ethnicity,
                age_in_years=subject_screening.age_in_years,
                creatinine_value=self.creatinine_value,
                creatinine_units=self.creatinine_units,
            ).value
            self.egfr_units = EGFR_UNITS
            if is_baseline(self):
                self.egfr_percent_change = 0.0
            else:
                subject_identifier = self.subject_visit.subject_identifier
                baseline_obj = self.__class__.objects.get(
                    subject_visit__subject_identifier=subject_identifier,
                    subject_visit__visit_code=DAY1,
                    subject_visit__visit_code_sequence=0,
                )
                self.egfr_percent_change = egfr_percent_change(
                    float(self.egfr_value), float(baseline_obj.egfr_value)
                )
                if self.egfr_percent_change >= 0.20:
                    self.create_or_update_egfr_notification()
        super().save(*args, **kwargs)

    def create_or_update_egfr_notification(self):
        model_cls = django_apps.get_model("meta_subject.egfrnotification")
        with transaction.atomic():
            try:
                obj = model_cls.objects.get(subject_visit=self.subject_visit)
            except ObjectDoesNotExist:
                obj = model_cls.objects.create(
                    subject_visit=self.subject_visit,
                    report_datetime=self.report_datetime,
                    creatinine_date=self.assay_datetime.date(),
                    egfr_percent_change=self.egfr_percent_change,
                    report_status=NEW,
                    consent_version=self.consent_version,
                )
            else:
                obj.egfr_percent_change = self.egfr_percent_change
                obj.creatinine_date = self.assay_datetime.date()
                obj.save()
            finally:
                if obj.report_status != CLOSED:
                    obj.action_item.status = OPEN
                    obj.save()

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: RFT"
        verbose_name_plural = "Blood Results: RFT"
