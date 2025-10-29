from datetime import datetime
from zoneinfo import ZoneInfo

from clinicedc_constants import YES
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_appointment.constants import NEW_APPT
from edc_lab_panel.panels import hba1c_panel, insulin_panel
from edc_metadata.metadata_rules import PersistantSingletonMixin
from edc_sites.site import sites
from edc_visit_schedule.constants import (
    DAY1,
    MONTH1,
    MONTH3,
    MONTH6,
    MONTH12,
    MONTH18,
    MONTH24,
    MONTH30,
    MONTH36,
    MONTH48,
    WEEK2,
)
from edc_visit_schedule.utils import is_baseline

from meta_visit_schedule.constants import MONTH39, MONTH42, MONTH45


def hba1c_crf_required_at_baseline(visit):
    model_name = "meta_subject.bloodresultshba1c"
    screening_model_cls = django_apps.get_model("meta_screening.subjectscreening")
    bloodresults_model_cls = django_apps.get_model(model_name)
    required = False
    if is_baseline(instance=visit):
        try:
            screening_model_cls.objects.get(
                subject_identifier=visit.subject_identifier,
                hba1c_value__isnull=True,
            )
        except ObjectDoesNotExist:
            pass
        else:
            try:
                obj = bloodresults_model_cls.objects.get(
                    subject_visit__visit_code=DAY1,
                    subject_visit__visit_code_sequence=0,
                )
            except ObjectDoesNotExist:
                required = True
            else:
                if not obj.hba1c_value:
                    required = True
    return required


def hba1c_requisition_required_at_baseline(visit):
    screening_model_cls = django_apps.get_model("meta_screening.subjectscreening")
    required = False
    if is_baseline(instance=visit):
        try:
            screening_model_cls.objects.get(
                subject_identifier=visit.subject_identifier,
                hba1c_value__isnull=False,
            )
        except ObjectDoesNotExist:
            required = True
    return required


class Predicates(PersistantSingletonMixin):
    app_label = "meta_subject"

    @staticmethod
    def next_appt_required(visit, **kwargs):  # noqa: ARG004
        return visit.appointment.next and visit.appointment.next.appt_status == NEW_APPT

    @staticmethod
    def glucose_required(visit, **kwargs):  # noqa: ARG004
        return visit.visit_code in [MONTH12, MONTH24, MONTH36, MONTH48]

    @staticmethod
    def glucose_fbg_required(visit, **kwargs):  # noqa: ARG004
        return visit.report_datetime >= datetime(
            2024, 3, 4, tzinfo=ZoneInfo("UTC")
        ) and visit.visit_code in [MONTH6, MONTH18, MONTH30, MONTH42]

    @staticmethod
    def pregnancy_notification_exists(visit, **kwargs):  # noqa: ARG004
        model_cls = django_apps.get_model("meta_prn.pregnancynotification")
        try:
            model_cls.objects.get(subject_identifier=visit.subject_identifier, delivered=False)
        except ObjectDoesNotExist:
            required = False
        else:
            required = True
        return required

    @staticmethod
    def hba1c_crf_required(visit, **kwargs) -> bool:  # noqa: ARG004
        """Require at baseline visit if not recorded on the
        screening form.
        """
        required = hba1c_crf_required_at_baseline(visit)
        if (
            not required
            and visit.appointment.visit_code != DAY1
            and visit.appointment.visit_code_sequence == 0
            and visit.appointment.visit_code
            in visit.schedule.crf_required_at("meta_subject.bloodresultshba1c")
        ):
            required = True
        return required

    @staticmethod
    def hba1c_requisition_required(visit, **kwargs) -> bool:  # noqa: ARG004
        """Require at baseline visit if not recorded on the
        screening form.
        """
        required = hba1c_requisition_required_at_baseline(visit)
        if (
            not required
            and visit.appointment.visit_code != DAY1
            and visit.appointment.visit_code_sequence == 0
            and visit.appointment.visit_code
            in visit.schedule.requisition_required_at(hba1c_panel)
        ):
            required = True
        return required

    @staticmethod
    def insulin_crf_required(visit, **kwargs) -> bool:  # noqa: ARG004
        """Require at baseline visit"""
        required = False
        if (
            visit.site.id
            in [
                sites.get_by_attr("name", "mwananyamala").site_id,
                sites.get_by_attr("name", "temeke").site_id,
            ]
            and visit.appointment.visit_code
            in visit.schedule.crf_required_at("meta_subject.bloodresultsins")
            and visit.appointment.visit_code_sequence == 0
        ):
            required = True
        return required

    @staticmethod
    def insulin_requisition_required(visit, **kwargs) -> bool:  # noqa: ARG004
        """Require at baseline visit"""
        required = False
        if (
            visit.site.id
            in [
                sites.get_by_attr("name", "mwananyamala").site_id,
                sites.get_by_attr("name", "temeke").site_id,
            ]
            and visit.appointment.visit_code
            in visit.schedule.requisition_required_at(insulin_panel)
            and visit.appointment.visit_code_sequence == 0
        ):
            required = True
        return required

    def health_economics_required(self, visit, **kwargs) -> bool:  # noqa: ARG002
        """Returns true if HE was not completed at week 2"""

        required = False
        if (
            visit.appointment.visit_code == WEEK2
            and visit.appointment.visit_code_sequence == 0
        ):
            required = True
        elif (
            visit.appointment.visit_code == MONTH1
            and visit.appointment.visit_code_sequence == 0
        ):
            model_cls = django_apps.get_model(f"{self.app_label}.healtheconomicssimple")
            try:
                model_cls.objects.get(
                    subject_visit__subject_identifier=visit.subject_identifier,
                    subject_visit__visit_code=WEEK2,
                    subject_visit__visit_code_sequence=0,
                )
            except ObjectDoesNotExist:
                required = True
        return required

    def health_economics_update_required(self, visit, **kwargs) -> bool:  # noqa: ARG002
        """Returns true if `healtheconomicsupdate` was not completed at
        month 3 or ever.

        `healtheconomicsupdate` is a singleton CRF.
        """
        required = False
        model_cls = django_apps.get_model(f"{self.app_label}.healtheconomicsupdate")
        try:
            obj = model_cls.objects.get(
                subject_visit__subject_identifier=visit.subject_identifier,
            )
        except ObjectDoesNotExist:
            obj = None
        if (
            not obj
            and visit.appointment.visit_code_sequence == 0
            and visit.appointment.visit_code not in [DAY1, WEEK2, MONTH1]
        ):
            required = True
        return required

    def mnsi_required(self, visit, **kwargs) -> bool:  # noqa: ARG002
        """Returns True if:
        - MNSI assessment not performed in the 1, 3 or 6M visits
        - MNSI assessment not performed in the 36, 39, 42, 45M visits
        - MNSI assessment not performed in the 48M visit
        """
        model_cls = django_apps.get_model(f"{self.app_label}.mnsi")
        required = True

        if self.offschedule_today(visit):
            return True
        if visit.visit_code_sequence != 0 or visit.visit_code not in [
            MONTH1,
            MONTH3,
            MONTH6,
            MONTH36,
            MONTH39,
            MONTH42,
            MONTH45,
            MONTH48,
        ]:
            required = False
        elif visit.visit_code in [MONTH1, MONTH3, MONTH6]:
            objs = model_cls.objects.filter(
                subject_visit__subject_identifier=visit.subject_identifier,
                subject_visit__visit_code__in=[MONTH1, MONTH3, MONTH6],
                subject_visit__visit_code_sequence=0,
            )
            for obj in objs:
                if obj.mnsi_performed == YES:
                    required = False
                    break
        elif visit.visit_code in [MONTH36, MONTH39, MONTH42, MONTH45]:
            objs = model_cls.objects.filter(
                subject_visit__subject_identifier=visit.subject_identifier,
                subject_visit__visit_code__in=[MONTH36, MONTH39, MONTH42, MONTH45],
                subject_visit__visit_code_sequence=0,
            )
            for obj in objs:
                if obj.mnsi_performed == YES:
                    required = False
                    break
        return required

    def sf12_required(self, visit, **kwargs):  # noqa: ARG002
        model = f"{self.app_label}.sf12"
        if self.offschedule_today(visit) or (
            visit.visit_code_sequence == 0 and visit.visit_code in [MONTH36, MONTH48]
        ):
            return True
        return self.persistant_singleton_required(
            visit, model=model, exclude_visit_codes=[DAY1]
        )

    def eq5d3l_required(self, visit, **kwargs):  # noqa: ARG002
        model = f"{self.app_label}.eq5d3l"
        if self.offschedule_today(visit) or (
            visit.visit_code_sequence == 0 and visit.visit_code in [MONTH36, MONTH48]
        ):
            return True
        return self.persistant_singleton_required(
            visit, model=model, exclude_visit_codes=[DAY1]
        )

    def offschedule_today(self, visit):
        try:
            obj = django_apps.get_model(f"{self.app_label}.nextappointment").objects.get(
                subject_visit=visit
            )
        except ObjectDoesNotExist:
            pass
        else:
            if obj.offschedule_today == YES:
                return True
        return False
