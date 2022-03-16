from edc_visit_schedule import VisitSchedule

from ...constants import VISIT_SCHEDULE
from .schedule import schedule

visit_schedule = VisitSchedule(
    name=VISIT_SCHEDULE,
    verbose_name="Meta",
    offstudy_model="edc_offstudy.subjectoffstudy",
    death_report_model="meta_ae.deathreport",
    locator_model="edc_locator.subjectlocator",
    previous_visit_schedule=None,
)

visit_schedule.add_schedule(schedule)
