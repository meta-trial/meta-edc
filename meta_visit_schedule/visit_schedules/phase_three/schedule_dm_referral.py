from dateutil.relativedelta import relativedelta
from edc_facility.constants import FIVE_DAY_CLINIC
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Crf, CrfCollection, Visit

from meta_consent.consents import consent_v1

from ...constants import DM_FOLLOWUP, SCHEDULE_DM_REFERRAL
from .crfs import crfs_missed
from .crfs import crfs_prn
from .crfs import crfs_prn as default_crfs_prn

crfs = CrfCollection(
    Crf(show_order=100, model="meta_subject.dmfollowup"),
    name="dmfollowup",
)

schedule = Schedule(
    name=SCHEDULE_DM_REFERRAL,
    verbose_name="Diabetes Referral and Follow-up",
    onschedule_model="meta_prn.onscheduledmreferral",
    offschedule_model="meta_prn.offscheduledmreferral",
    consent_definitions=[consent_v1],
    appointment_model="edc_appointment.appointment",
    base_timepoint=300,
)


visit = Visit(
    code=DM_FOLLOWUP,
    title="Diabetes post-referral follow-up",
    timepoint=300,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(months=12),
    crfs=crfs,
    crfs_prn=crfs_prn or default_crfs_prn,
    crfs_missed=crfs_missed,
    facility_name=FIVE_DAY_CLINIC,
)


schedule.add_visit(visit=visit)
