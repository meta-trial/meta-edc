from dateutil.relativedelta import relativedelta
from edc_facility.constants import FIVE_DAY_CLINIC
from edc_visit_schedule import Schedule
from edc_visit_schedule import Visit as BaseVisit

from ...constants import (
    DAY1,
    MONTH1,
    MONTH3,
    MONTH6,
    MONTH9,
    MONTH12,
    MONTH15,
    MONTH18,
    MONTH21,
    MONTH24,
    MONTH27,
    MONTH30,
    MONTH33,
    MONTH36,
    SCHEDULE,
    WEEK2,
)
from .crfs import (
    crfs_1m,
    crfs_3m,
    crfs_6m,
    crfs_9m,
    crfs_12m,
    crfs_15m,
    crfs_18m,
    crfs_21m,
    crfs_24m,
    crfs_27m,
    crfs_30m,
    crfs_33m,
    crfs_36m,
    crfs_d1,
    crfs_missed,
)
from .crfs import crfs_prn as default_crfs_prn
from .crfs import crfs_unscheduled as default_crfs_unscheduled
from .crfs import crfs_w2
from .requisitions import (
    requisitions_1m,
    requisitions_3m,
    requisitions_6m,
    requisitions_9m,
    requisitions_12m,
    requisitions_15m,
    requisitions_18m,
    requisitions_21m,
    requisitions_24m,
    requisitions_27m,
    requisitions_30m,
    requisitions_33m,
    requisitions_36m,
    requisitions_d1,
)
from .requisitions import requisitions_prn as default_requisitions_prn
from .requisitions import requisitions_unscheduled as default_requisitions_unscheduled
from .requisitions import requisitions_w2


class Visit(BaseVisit):
    def __init__(
        self,
        crfs_unscheduled=None,
        requisitions_unscheduled=None,
        crfs_prn=None,
        requisitions_prn=None,
        allow_unscheduled=None,
        **kwargs,
    ):
        super().__init__(
            allow_unscheduled=True if allow_unscheduled is None else allow_unscheduled,
            crfs_unscheduled=crfs_unscheduled or default_crfs_unscheduled,
            requisitions_unscheduled=requisitions_unscheduled
            or default_requisitions_unscheduled,
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
    offschedule_model="meta_prn.offschedule",
    consent_model="meta_consent.subjectconsent",
    appointment_model="edc_appointment.appointment",
    offstudymedication_model="meta_prn.offstudymedication",
)


# TODO: do not allow a few days between consent and first appt

visit000 = Visit(
    code=DAY1,
    title="Day 1",
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions_d1,
    crfs=crfs_d1,
    facility_name=FIVE_DAY_CLINIC,
)

visit002 = Visit(
    code=WEEK2,
    title="Week 2",
    timepoint=1,
    rbase=relativedelta(weeks=2),
    rlower=relativedelta(days=3),
    rupper=relativedelta(days=4),
    requisitions=requisitions_w2,
    crfs=crfs_w2,
    facility_name=FIVE_DAY_CLINIC,
)

visit01 = Visit(
    code=MONTH1,
    title="Month 1",
    timepoint=2,
    rbase=relativedelta(months=1),
    rlower=relativedelta(days=10),
    rupper=relativedelta(days=30),
    requisitions=requisitions_1m,
    crfs=crfs_1m,
    facility_name=FIVE_DAY_CLINIC,
)


visit03 = Visit(
    code=MONTH3,
    title="Month 3",
    timepoint=3,
    rbase=relativedelta(months=3),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=2),
    requisitions=requisitions_3m,
    crfs=crfs_3m,
    facility_name=FIVE_DAY_CLINIC,
)

visit06 = Visit(
    code=MONTH6,
    title="Month 6",
    timepoint=4,
    rbase=relativedelta(months=6),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=2),
    requisitions=requisitions_6m,
    crfs=crfs_6m,
    facility_name=FIVE_DAY_CLINIC,
)

visit09 = Visit(
    code=MONTH9,
    title="Month 9",
    timepoint=5,
    rbase=relativedelta(months=9),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=2),
    requisitions=requisitions_9m,
    crfs=crfs_9m,
    facility_name=FIVE_DAY_CLINIC,
)
visit12 = Visit(
    code=MONTH12,
    title="Month 12",
    timepoint=6,
    rbase=relativedelta(months=12),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=2),
    requisitions=requisitions_12m,
    crfs=crfs_12m,
    facility_name=FIVE_DAY_CLINIC,
)

visit15 = Visit(
    code=MONTH15,
    title="Month 15",
    timepoint=7,
    rbase=relativedelta(months=15),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=2),
    requisitions=requisitions_15m,
    crfs=crfs_15m,
    facility_name=FIVE_DAY_CLINIC,
)

visit18 = Visit(
    code=MONTH18,
    title="Month 18",
    timepoint=8,
    rbase=relativedelta(months=18),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=2),
    requisitions=requisitions_18m,
    crfs=crfs_18m,
    facility_name=FIVE_DAY_CLINIC,
)

visit21 = Visit(
    code=MONTH21,
    title="Month 21",
    timepoint=9,
    rbase=relativedelta(months=21),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=2),
    requisitions=requisitions_21m,
    crfs=crfs_21m,
    facility_name=FIVE_DAY_CLINIC,
)

visit24 = Visit(
    code=MONTH24,
    title="Month 24",
    timepoint=10,
    rbase=relativedelta(months=24),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=2),
    requisitions=requisitions_24m,
    crfs=crfs_24m,
    facility_name=FIVE_DAY_CLINIC,
)

visit27 = Visit(
    code=MONTH27,
    title="Month 27",
    timepoint=11,
    rbase=relativedelta(months=27),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=2),
    requisitions=requisitions_27m,
    crfs=crfs_27m,
    facility_name=FIVE_DAY_CLINIC,
)

visit30 = Visit(
    code=MONTH30,
    title="Month 30",
    timepoint=12,
    rbase=relativedelta(months=30),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=2),
    requisitions=requisitions_30m,
    crfs=crfs_30m,
    facility_name=FIVE_DAY_CLINIC,
)

visit33 = Visit(
    code=MONTH33,
    title="Month 33",
    timepoint=13,
    rbase=relativedelta(months=33),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=2),
    requisitions=requisitions_33m,
    crfs=crfs_33m,
    facility_name=FIVE_DAY_CLINIC,
)

visit36 = Visit(
    code=MONTH36,
    title="Month 36",
    timepoint=14,
    rbase=relativedelta(months=36),
    rlower=relativedelta(months=1),
    rupper=relativedelta(months=1),
    requisitions=requisitions_36m,
    crfs=crfs_36m,
    facility_name=FIVE_DAY_CLINIC,
)


visits = [
    visit000,
    visit002,
    visit01,
    visit03,
    visit06,
    visit09,
    visit12,
    visit15,
    visit18,
    visit21,
    visit24,
    visit27,
    visit30,
    visit33,
    visit36,
]
for visit in visits:
    schedule.add_visit(visit=visit)
