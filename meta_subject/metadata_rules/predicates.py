from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import FEMALE, YES
from edc_lab_panel.panels import hba1c_panel
from edc_metadata.metadata_rules import PredicateCollection
from edc_registration.models import RegisteredSubject
from edc_visit_schedule.constants import DAY1, MONTH1, MONTH3, MONTH6, WEEK2
from edc_visit_schedule.utils import is_baseline

from meta_visit_schedule.constants import SCHEDULE_PREGNANCY


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


class Predicates(PredicateCollection):

    app_label = "meta_subject"
    visit_model = "meta_subject.subjectvisit"

    @staticmethod
    def pregnancy_notification_exists(visit, **kwargs):
        model_cls = django_apps.get_model("meta_prn.pregnancynotification")
        try:
            model_cls.objects.get(subject_identifier=visit.subject_identifier, delivered=False)
        except ObjectDoesNotExist:
            required = False
        else:
            required = True
        return required

    @staticmethod
    def hba1c_crf_required(visit, **kwargs) -> bool:
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
    def hba1c_requisition_required(visit, **kwargs) -> bool:
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

    def health_economics_required(self, visit, **kwargs) -> bool:
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

    @staticmethod
    def urine_pregnancy_required(visit, **kwargs) -> bool:
        """Returns True if required.

        Bu default is not required at baseline, otherwise at 1, 3, 6, etc"""
        registered_subject = RegisteredSubject.objects.get(
            subject_identifier=visit.subject_identifier
        )
        if (
            registered_subject.gender == FEMALE
            and visit.schedule_name != SCHEDULE_PREGNANCY
            and not is_baseline(instance=visit)
            and not (
                visit.appointment.visit_code == WEEK2
                and visit.appointment.visit_code_sequence == 0
            )
        ):
            return True
        else:
            return False

    def mnsi_required(self, visit, **kwargs) -> bool:
        """Returns True if MNSI assessment was not performed at the
        1M, 3M or 6M visits.
        """
        required = True
        if (
            visit.appointment.visit_code in [MONTH1, MONTH3, MONTH6]
        ) and visit.appointment.visit_code_sequence == 0:
            model_cls = django_apps.get_model(f"{self.app_label}.mnsi")
            objs = model_cls.objects.filter(
                subject_visit__subject_identifier=visit.subject_identifier,
                subject_visit__visit_code__in=[MONTH1, MONTH3, MONTH6],
                subject_visit__visit_code_sequence=0,
            )
            for obj in objs:
                if obj.mnsi_performed == YES:
                    required = False
                    break
        return required
