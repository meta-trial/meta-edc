from edc_visit_schedule import VisitSchedule, site_visit_schedules

from .schedule import schedule

VISIT_SCHEDULE = "visit_schedule"


visit_schedule = VisitSchedule(
    name=VISIT_SCHEDULE,
    verbose_name="Meta",
    offstudy_model="edc_offstudy.subjectoffstudy",
    death_report_model="meta_ae.deathreport",
    locator_model="edc_locator.subjectlocator",
    previous_visit_schedule=None,
)

visit_schedule.add_schedule(schedule)

site_visit_schedules.register(visit_schedule)
