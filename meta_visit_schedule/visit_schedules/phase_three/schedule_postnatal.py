from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Schedule, Visit

from ...constants import POSTNATAL, SCHEDULE_POSTNATAL
from .crfs import crfs_36m, crfs_missed
from .crfs import crfs_prn
from .crfs import crfs_prn as default_crfs_prn

schedule = Schedule(
    name=SCHEDULE_POSTNATAL,
    verbose_name="Postnatal 36m Follow-up",
    onschedule_model="meta_prn.onschedulepostnatal",
    offschedule_model="meta_prn.offschedulepostnatal",
    consent_model="meta_consent.subjectconsent",
    appointment_model="edc_appointment.appointment",
)

# TODO: appointment date will be 36m from consent

visit = Visit(
    code=POSTNATAL,
    title="Postnatal 36m Followup",
    timepoint=300,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(months=1),
    crfs=crfs_36m,
    crfs_prn=crfs_prn or default_crfs_prn,
    crfs_missed=crfs_missed,
    facility_name="7-day-clinic",
)


schedule.add_visit(visit=visit)
