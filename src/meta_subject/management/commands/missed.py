import urllib.parse
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from edc_appointment.constants import NEW_APPT
from edc_appointment.models import Appointment
from edc_registration.models import RegisteredSubject
from edc_utils import formatted_date, get_utcnow
from edc_visit_tracking.constants import MISSED_VISIT
from tqdm import tqdm

from meta_prn.models import EndOfStudy, OffSchedule, OffStudyMedication
from meta_subject.models import SubjectVisit, SubjectVisitMissed

urllib.parse.quote("D-cHO$?N-1cOYHl^2^GDbZ:o-^X")

visit_codes = [
    "1000",
    "1005",
    "1010",
    "1030",
    "1060",
    "1090",
    "1120",
    "1150",
    "1180",
    "1210",
    "1240",
    "1270",
    "1300",
    "1330",
    "1360",
]


def is_sublist(a, b):
    if not a:
        return True
    if not b:
        return False
    return b[: len(a)] == a or is_sublist(a, b[1:])


def get_missed_visit_codes(subject_identifier: str) -> list[str]:
    """Return visit codes from SubjectVisitMissed
    reports for this subject.
    """
    return [
        missed_obj.subject_visit.visit_code
        for missed_obj in SubjectVisitMissed.objects.filter(
            subject_visit__subject_identifier=subject_identifier
        ).order_by("report_datetime")
    ]


def get_missed_visit_codes_from_subject_visit(subject_identifier: str) -> list[str]:
    return [
        missed_obj.visit_code
        for missed_obj in SubjectVisit.objects.filter(
            subject_identifier=subject_identifier, reason=MISSED_VISIT
        ).order_by("report_datetime")
    ]


def run():
    result = {}
    total = RegisteredSubject.objects.all().count()
    for obj in tqdm(
        RegisteredSubject.objects.all().order_by("subject_identifier"), total=total
    ):
        missed_visit_codes = get_missed_visit_codes(obj.subject_identifier)
        if len(missed_visit_codes) > 2 and is_sublist(missed_visit_codes, visit_codes):
            result.update({obj.subject_identifier: missed_visit_codes})
    return result


def run2():
    result = {}
    total = RegisteredSubject.objects.all().count()
    for obj in tqdm(
        RegisteredSubject.objects.all().order_by("subject_identifier"), total=total
    ):
        missed_visit_codes = get_missed_visit_codes_from_subject_visit(obj.subject_identifier)
        if len(missed_visit_codes) > 2 and is_sublist(missed_visit_codes, visit_codes):
            result.update({obj.subject_identifier: missed_visit_codes})
    return result


def new_appointments():
    result = {}
    total = RegisteredSubject.objects.all().count()
    for obj in tqdm(
        RegisteredSubject.objects.all().order_by("subject_identifier"), total=total
    ):
        codes = []
        for appointment in Appointment.objects.filter(
            subject_identifier=obj.subject_identifier,
            appt_status=NEW_APPT,
            timepoint_datetime__lte=get_utcnow(),
        ).order_by("timepoint_datetime"):
            codes.append(appointment.visit_code)
            if len(codes) >= 2 and is_sublist(codes, visit_codes):
                result.update({obj.subject_identifier: codes})
    return result


def new_appointments_within(months: int):
    result = {}
    total = RegisteredSubject.objects.all().count()
    for obj in tqdm(
        RegisteredSubject.objects.all().order_by("subject_identifier"), total=total
    ):
        codes = []
        appointment = (
            Appointment.objects.filter(
                subject_identifier=obj.subject_identifier,
                appt_status=NEW_APPT,
                timepoint_datetime__lte=get_utcnow() - relativedelta(months=months),
            )
            .order_by("timepoint_datetime")
            .last()
        )
        if appointment:
            codes.append(appointment.visit_code)
            result.update({obj.subject_identifier: codes})
    return result


class Result:
    """Used with run3."""

    def __init__(  # noqa: PLR0913
        self,
        subject_identifier: str,
        sid: str,
        first_visit: datetime,
        first_missed_visit: datetime,
        last_missed_visit: datetime,
        last_visit: datetime,
        off_meds: date,
        offschedule: date,
        offstudy: date,
        codes: list[str],
    ):
        self.subject_identifier = subject_identifier
        self.sid = sid
        if last_missed_visit and first_missed_visit:
            self.missed = (last_missed_visit - first_missed_visit).days
        else:
            self.missed = 0
        self.onstudy = (last_visit - first_visit).days
        self.attended = self.onstudy - self.missed
        if last_missed_visit:
            self.attended_after_missed = last_visit > last_missed_visit
        else:
            self.attended_after_missed = False
        self.offmeds = (off_meds - first_visit.date()).days if off_meds else 0
        self.offschedule = (offschedule - first_visit.date()).days if offschedule else 0
        self.offstudy = (offstudy - first_visit.date()).days if offstudy else 0
        self.last_visit_date = last_visit.date()
        self.offstudy_date = offstudy
        self.visit_codes = codes

    def __str__(self):
        return f"{self.subject_identifier} {self.visit_codes}"

    def formatted(self) -> str:
        """Copy/paste output into text file"""
        return (
            f"{self.subject_identifier},{self.sid},{self.onstudy},{self.missed},"
            f"{self.attended_after_missed},{self.offmeds},{self.offschedule},"
            f"{self.offstudy},{formatted_date(self.offstudy_date)},"
            f"{';'.join(self.visit_codes)}"
        )


def runner(result=None):
    """
    result = runner(new_appointments())
    for r in result.values():
        print(r.formatted())
    """
    new_result = {}
    for subject_identifier, vcodes in result.items():
        sid = RegisteredSubject.objects.get(subject_identifier=subject_identifier).sid
        first_visit = (
            SubjectVisit.objects.filter(subject_identifier=subject_identifier)
            .order_by("report_datetime")
            .first()
        ).report_datetime
        try:
            first_missed_visit = SubjectVisit.objects.get(
                subject_identifier=subject_identifier,
                visit_code=vcodes[0],
                reason=MISSED_VISIT,
            ).report_datetime
        except ObjectDoesNotExist:
            first_missed_visit = 0
        try:
            last_missed_visit = SubjectVisit.objects.get(
                subject_identifier=subject_identifier,
                visit_code=vcodes[-1],
                reason=MISSED_VISIT,
            ).report_datetime
        except ObjectDoesNotExist:
            last_missed_visit = 0
        last_visit = (
            SubjectVisit.objects.filter(subject_identifier=subject_identifier)
            .order_by("report_datetime")
            .last()
        ).report_datetime
        try:
            off_meds = OffStudyMedication.objects.get(
                subject_identifier=subject_identifier
            ).last_dose_date
        except ObjectDoesNotExist:
            off_meds = None
        try:
            offschedule = OffSchedule.objects.get(
                subject_identifier=subject_identifier
            ).offschedule_datetime
        except ObjectDoesNotExist:
            offschedule = None
        else:
            offschedule = offschedule.date()

        try:
            offstudy = EndOfStudy.objects.get(
                subject_identifier=subject_identifier
            ).last_seen_date
        except ObjectDoesNotExist:
            offstudy = None

        new_result.update(
            {
                subject_identifier: Result(
                    subject_identifier,
                    sid,
                    first_visit,
                    first_missed_visit,
                    last_missed_visit,
                    last_visit,
                    off_meds,
                    offschedule,
                    offstudy,
                    vcodes,
                )
            }
        )
    return new_result
