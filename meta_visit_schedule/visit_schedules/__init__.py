import sys

from django.core.management import color_style
from edc_visit_schedule import site_visit_schedules

from meta_edc.meta_version import get_meta_version

style = color_style()

if get_meta_version() == 2:
    from .phase_two import SCHEDULE, VISIT_SCHEDULE, schedule, visit_schedule

    sys.stdout.write(
        style.SUCCESS("Notice: loading visit schedule for phase 2 **** \n")
    )
elif get_meta_version() == 3:
    from .phase_three import SCHEDULE, VISIT_SCHEDULE, schedule, visit_schedule

    sys.stdout.write(
        style.SUCCESS("Notice: loading visit schedule for phase 3 **** \n")
    )
site_visit_schedules.register(visit_schedule)
