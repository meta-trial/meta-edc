import sys

from django.core.management import color_style
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .phase_three import schedule, visit_schedule

style = color_style()

sys.stdout.write(style.SUCCESS("Notice: loading visit schedule for phase 3 **** \n"))
site_visit_schedules.register(visit_schedule)

__all__ = ["schedule", "visit_schedule"]
