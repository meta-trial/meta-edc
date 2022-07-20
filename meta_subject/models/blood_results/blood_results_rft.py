from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from edc_constants.constants import NEW
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_lab.model_mixins import CrfWithRequisitionModelMixin
from edc_lab_panel.panels import rft_panel
from edc_lab_results import BLOOD_RESULTS_RFT_ACTION
from edc_lab_results.model_mixins import (
    BloodResultsModelMixin,
    CreatinineModelMixin,
    EgfrDropModelMixin,
    EgfrModelMixin,
    UreaModelMixin,
    UricAcidModelMixin,
)
from edc_model import models as edc_models
from edc_registration.models import RegisteredSubject
from edc_reportable import EgfrCkdEpi, site_reportables
from edc_reportable.calculators import egfr_percent_change
from edc_reportable.units import EGFR_UNITS, PERCENT
from edc_screening.utils import get_subject_screening_model_cls
from edc_visit_schedule.constants import DAY1
from edc_visit_schedule.utils import is_baseline


class BloodResultsRft(
    CrfWithActionModelMixin,
    CreatinineModelMixin,
    EgfrModelMixin,
    EgfrDropModelMixin,
    UreaModelMixin,
    UricAcidModelMixin,
    CrfWithRequisitionModelMixin,
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
            self.egfr_value = EgfrCkdEpi(
                gender=subject_screening.gender,
                ethnicity=subject_screening.ethnicity,
                age_in_years=subject_screening.age_in_years,
                creatinine_value=self.creatinine_value,
                creatinine_units=self.creatinine_units,
            ).value
            self.egfr_units = EGFR_UNITS
            self.egfr_drop_units = PERCENT
            if is_baseline(self):
                self.egfr_drop_value = 0.0
            else:
                subject_identifier = self.subject_visit.subject_identifier
                baseline_obj = self.__class__.objects.get(
                    subject_visit__subject_identifier=subject_identifier,
                    subject_visit__visit_code=DAY1,
                    subject_visit__visit_code_sequence=0,
                )
                opts = dict(
                    gender=self.registered_subject.gender,
                    dob=self.registered_subject.dob,
                    report_datetime=self.subject_visit.report_datetime,
                )

                reference_grp = site_reportables.get(
                    self.get_reference_range_collection_name()
                ).get("egfr")
                opts.update(units=self.egfr_units)
                grade_obj = reference_grp.get_grade(self.egfr_value, **opts)
                if grade_obj:
                    self.egfr_grade = grade_obj.grade

                self.egfr_drop_value = egfr_percent_change(
                    float(self.egfr_value), float(baseline_obj.egfr_value)
                )

                reference_grp = site_reportables.get(
                    self.get_reference_range_collection_name()
                ).get("egfr_drop")
                opts.update(units=self.egfr_drop_units)
                grade_obj = reference_grp.get_grade(self.egfr_drop_value, **opts)
                if grade_obj:
                    self.egfr_drop_grade = grade_obj.grade

                if self.egfr_drop_value >= 0.20:
                    self.create_or_update_egfr_notification()
        super().save(*args, **kwargs)

    @property
    def registered_subject(self):
        return RegisteredSubject.objects.get(
            subject_identifier=self.subject_visit.subject_identifier
        )

    def create_or_update_egfr_notification(self):
        model_cls = django_apps.get_model("meta_subject.egfrdropnotification")
        with transaction.atomic():
            try:
                obj = model_cls.objects.get(subject_visit=self.subject_visit)
            except ObjectDoesNotExist:
                model_cls.objects.create(
                    subject_visit=self.subject_visit,
                    report_datetime=self.report_datetime,
                    creatinine_date=self.assay_datetime.date(),
                    egfr_percent_change=self.egfr_drop_value,
                    report_status=NEW,
                    consent_version=self.consent_version,
                )
            else:
                obj.egfr_percent_change = self.egfr_drop_value
                obj.creatinine_date = self.assay_datetime.date()
                obj.save()

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: RFT"
        verbose_name_plural = "Blood Results: RFT"
