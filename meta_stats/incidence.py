from edc_registration.models import RegisteredSubject

from meta_subject.models import Glucose


def get_sequential_fgb():
    """look for anyone with two or more sequential FBG measurements"""

    for rs in RegisteredSubject.objects.all().order_by("subject_identifier"):
        values = []
        for index, glucose in enumerate(
            Glucose.objects.filter(
                subject_visit__subject_identifier=rs.subject_identifier
            ).order_by("report_datetime")
        ):
            values.append(glucose.fbg_value)
