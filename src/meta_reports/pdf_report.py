from textwrap import fill

from edc_pdf_reports.crf_pdf_report import CrfPdfReport
from edc_randomization.auth_objects import RANDO_UNBLINDED
from edc_randomization.models import RandomizationList
from reportlab.lib.units import cm
from reportlab.platypus import Table

from meta_subject.models import FollowupVitals


def get_weight_for_timepoint(subject_identifier=None, reference_dt=None):
    qs = FollowupVitals.objects.filter(
        subject_visit__appointment__subject_identifier=subject_identifier,
        report_datetime__lte=reference_dt,
    ).order_by("-report_datetime")
    if qs:
        return qs[0].weight
    return None


class MetaCrfPdfReport(CrfPdfReport):
    logo_data = {  # noqa: RUF012
        "app_label": "meta_edc",
        "filename": "meta_logo.png",
        "first_page": (4.0 * cm, 0.83 * cm),
        "later_pages": (3.0 * cm, 0.625 * cm),
    }

    def __init__(self, subject_identifier=None, **kwargs):
        super().__init__(**kwargs)
        self.subject_identifier = subject_identifier
        self.drug_assignment = RandomizationList.objects.get(
            subject_identifier=self.subject_identifier
        ).get_drug_assignment_display()

    def draw_demographics(self, story, **kwargs):  # noqa: ARG002
        model_obj = getattr(self, self.model_attr)
        weight = get_weight_for_timepoint(
            subject_identifier=self.subject_identifier,
            reference_dt=model_obj.report_datetime,
        )
        assignment = "*****************"
        if self.request.user.groups.filter(name=RANDO_UNBLINDED).exists():
            assignment = fill(self.drug_assignment, width=80)
        rows = [
            ["Subject:", self.subject_identifier],
            [
                "Gender/Age:",
                f"{self.registered_subject.get_gender_display()} {self.age}",
            ],
            ["Weight:", f"{weight} kg"],
            [
                "Study site:",
                f"{self.registered_subject.site.id}: "
                f"{self.registered_subject.site.name.title()}",
            ],
            [
                "Randomization date:",
                self.registered_subject.randomization_datetime.strftime("%Y-%m-%d %H:%M"),
            ],
            ["Assignment:", assignment],
        ]

        t = Table(rows, (4 * cm, 14 * cm))
        self.set_table_style(t, bg_cmd=self.bg_cmd)
        t.hAlign = "LEFT"
        story.append(t)
