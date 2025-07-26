from textwrap import fill

import inflect
from django.contrib.auth import get_user_model
from edc_constants.constants import OTHER, TUBERCULOSIS
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus.flowables import Spacer
from reportlab.platypus.para import Paragraph
from reportlab.platypus.tables import Table

from meta_ae.models import DeathReport as DeathReportModel

from .pdf_report import MetaCrfPdfReport

User = get_user_model()
p = inflect.engine()


class DeathPdfReport(MetaCrfPdfReport):
    model_attr = "death_report"

    def __init__(self, death_report=None, **kwargs):
        super().__init__(**kwargs)
        self.death_report = death_report

    def get_report_story(self, **kwargs):
        story = []

        self.draw_demographics(story)

        story.append(Spacer(0.1 * cm, 0.5 * cm))

        self._draw_section_one_header(story)

        self._draw_death_overview(story)

        story.append(Spacer(0.1 * cm, 0.5 * cm))

        self._draw_opinion(story)

        story.append(Spacer(0.1 * cm, 0.5 * cm))
        story.append(Spacer(0.1 * cm, 0.5 * cm))

        self._draw_audit_trail(story)

        story.append(Spacer(0.1 * cm, 0.5 * cm))

        self.draw_end_of_report(story)

        return story

    def _draw_section_one_header(self, story):
        t = Table([["Section 1: Death Report"]], (18 * cm))
        self.set_table_style(t, bg_cmd=self.bg_cmd)
        story.append(t)
        t = Table([[f"Prepared by {self.get_user(self.death_report)}."]], (18 * cm))
        self.set_table_style(t)
        story.append(t)

    def _draw_death_overview(self, story):
        # basics
        rows = [
            ["Reference:", self.death_report.identifier],
            [
                "Report date:",
                self.death_report.report_datetime.strftime("%Y-%m-%d %H:%M"),
            ],
            [
                "Death date:",
                self.death_report.death_datetime.strftime("%Y-%m-%d %H:%M"),
            ],
            ["Study day:", self.death_report.study_day],
            ["Death as inpatient:", self.death_report.death_as_inpatient],
        ]

        t = Table(rows, (4 * cm, 14 * cm))
        self.set_table_style(t, bg_cmd=self.bg_cmd)
        t.hAlign = "LEFT"
        story.append(t)

    def _draw_opinion(self, story):
        t = Table([["Section 2: Opinion of Local Study Doctor"]], (18 * cm))
        self.set_table_style(t, bg_cmd=self.bg_cmd)
        story.append(t)
        rows = []

        row = ["Main cause of death:"]
        if self.death_report.cause_of_death.short_name == OTHER:
            row.append(
                fill(
                    f"{self.death_report.cause_of_death.name}: "
                    f"{self.death_report.cause_of_death_other}",
                    width=80,
                )
            )
        else:
            row.append(fill(self.death_report.cause_of_death.name))

        rows.append(row)

        if self.death_report.cause_of_death == TUBERCULOSIS:
            rows.append(
                [
                    "If cause of death is TB, site of TB disease:",
                    self.death_report.get_tb_site_display(),
                ]
            )

        t = Table(rows, (4 * cm, 14 * cm))
        self.set_table_style(t, bg_cmd=self.bg_cmd)
        t.hAlign = "LEFT"
        story.append(t)

        self.draw_narrative(story, title="Narrative:", text=self.death_report.narrative)

    def _draw_audit_trail(self, story):
        s = self.styles["line_data_small"]
        t = Table(
            [
                [
                    Paragraph("Document", s),
                    Paragraph("Changed by", s),
                    Paragraph("Date", s),
                    Paragraph("Action", s),
                ]
            ],
            (3 * cm, 3 * cm, 3 * cm, 9 * cm),
        )
        self.set_table_style(t, bg_cmd=("BACKGROUND", (0, 0), (3, -1), colors.lightgrey))
        story.append(t)

        qs = DeathReportModel.history.filter(id=self.death_report.id).order_by("-history_date")
        for obj in qs:
            username = obj.user_created if obj.history_type == "+" else obj.user_modified
            t = Table(
                [
                    [
                        Paragraph(DeathReportModel._meta.verbose_name, s),
                        Paragraph(username, s),
                        Paragraph(obj.modified.strftime("%Y-%m-%d %H:%M"), s),
                        Paragraph(fill(self.history_change_message(obj), width=60), s),
                    ]
                ],
                (3 * cm, 3 * cm, 3 * cm, 9 * cm),
            )
            self.set_table_style(t)
            story.append(t)
