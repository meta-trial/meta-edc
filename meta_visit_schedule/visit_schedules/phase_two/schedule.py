from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Schedule
from edc_visit_schedule import Visit as BaseVisit

from ...constants import DAY1, MONTH1, MONTH3, MONTH6, MONTH9, MONTH12, WEEK2
from .crfs import crfs_1m, crfs_3m, crfs_6m, crfs_9m, crfs_12m, crfs_d1, crfs_missed
from .crfs import crfs_prn as default_crfs_prn
from .crfs import crfs_unscheduled as default_crfs_unscheduled
from .crfs import crfs_w2
from .requisitions import (
    requisitions_1m,
    requisitions_3m,
    requisitions_6m,
    requisitions_9m,
    requisitions_12m,
    requisitions_d1,
)
from .requisitions import requisitions_prn as default_requisitions_prn
from .requisitions import requisitions_w2

default_requisitions = None

SCHEDULE = "schedule"


class Visit(BaseVisit):
    def __init__(
        self,
        crfs_unscheduled=None,
        requisitions_unscheduled=None,
        crfs_prn=None,
        requisitions_prn=None,
        allow_unscheduled=None,
        **kwargs
    ):
        super().__init__(
            allow_unscheduled=True if allow_unscheduled is None else allow_unscheduled,
            crfs_unscheduled=crfs_unscheduled or default_crfs_unscheduled,
            requisitions_unscheduled=requisitions_unscheduled or default_requisitions,
            crfs_prn=crfs_prn or default_crfs_prn,
            requisitions_prn=requisitions_prn or default_requisitions_prn,
            crfs_missed=crfs_missed,
            **kwargs,
        )


# schedule for new participants
schedule = Schedule(
    name=SCHEDULE,
    verbose_name="Day 1 to Month 12 Follow-up",
    onschedule_model="meta_prn.onschedule",
    offschedule_model="meta_prn.endofstudy",
    consent_model="meta_consent.subjectconsent",
    appointment_model="edc_appointment.appointment",
)


visit0 = Visit(
    code=DAY1,
    title="Day 1",
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions_d1,
    crfs=crfs_d1,
    facility_name="7-day-clinic",
)

visit1 = Visit(
    code=WEEK2,
    title="Week 2",
    timepoint=1,
    rbase=relativedelta(weeks=2),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=4),
    requisitions=requisitions_w2,
    crfs=crfs_w2,
    facility_name="7-day-clinic",
)

visit2 = Visit(
    code=MONTH1,
    title="Month 1",
    timepoint=2,
    rbase=relativedelta(months=1),
    rlower=relativedelta(days=15),
    rupper=relativedelta(days=30),
    requisitions=requisitions_1m,
    crfs=crfs_1m,
    facility_name="7-day-clinic",
)


visit3 = Visit(
    code=MONTH3,
    title="Month 3",
    timepoint=3,
    rbase=relativedelta(months=3),
    rlower=relativedelta(days=15),
    rupper=relativedelta(days=30),
    requisitions=requisitions_3m,
    crfs=crfs_3m,
    facility_name="7-day-clinic",
)

visit4 = Visit(
    code=MONTH6,
    title="Month 6",
    timepoint=4,
    rbase=relativedelta(months=6),
    rlower=relativedelta(days=15),
    rupper=relativedelta(days=30),
    requisitions=requisitions_6m,
    crfs=crfs_6m,
    facility_name="7-day-clinic",
)

visit5 = Visit(
    code=MONTH9,
    title="Month 9",
    timepoint=5,
    rbase=relativedelta(months=9),
    rlower=relativedelta(days=15),
    rupper=relativedelta(days=30),
    requisitions=requisitions_9m,
    crfs=crfs_9m,
    facility_name="7-day-clinic",
)
visit6 = Visit(
    code=MONTH12,
    title="Month 12",
    timepoint=6,
    rbase=relativedelta(months=12),
    rlower=relativedelta(days=15),
    rupper=relativedelta(days=30),
    requisitions=requisitions_12m,
    crfs=crfs_12m,
    facility_name="7-day-clinic",
)


for visit in [
    visit0,
    visit1,
    visit2,
    visit3,
    visit4,
    visit5,
    visit6,
]:
    schedule.add_visit(visit=visit)
