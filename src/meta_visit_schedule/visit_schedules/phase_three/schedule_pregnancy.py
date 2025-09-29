from dateutil.relativedelta import relativedelta
from edc_facility.constants import FIVE_DAY_CLINIC
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Visit

from meta_consent.consents import consent_v1

from ...constants import DELIVERY, SCHEDULE_PREGNANCY
from .crfs import crfs_missed, crfs_prn
from .crfs import crfs_prn as default_crfs_prn
from .crfs_pregnancy import crfs_pregnancy

schedule = Schedule(
    name=SCHEDULE_PREGNANCY,
    verbose_name="Delivery and Birth Outcomes Follow-up",
    onschedule_model="meta_prn.onschedulepregnancy",
    offschedule_model="meta_prn.offschedulepregnancy",
    consent_definitions=[consent_v1],
    appointment_model="edc_appointment.appointment",
    base_timepoint=200,
)


visit = Visit(
    code=DELIVERY,
    title="Delivery",
    timepoint=200,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(months=24),
    crfs=crfs_pregnancy,
    crfs_prn=crfs_prn or default_crfs_prn,
    crfs_missed=crfs_missed,
    facility_name=FIVE_DAY_CLINIC,
)


schedule.add_visit(visit=visit)
