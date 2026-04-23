"""Generate the monitoring report PDF.

Usage::

    uv run manage.py generate_monitoring_report \\
        --output /path/to/monitoring_report_20260409.pdf \\
        --cutoff-date 2026-04-09 \\
        --data-download-date 2026-04-09 \\
        --end-of-trial-date 2026-05-31

Dates are interpreted as UTC. The ``--output`` path may be an explicit
file path or a directory; if a directory, the filename is derived from
the cutoff date as ``monitoring_report_YYYYMMDD.pdf``.

If ``--output`` is omitted the report is written to
``$META_ANALYSIS_FOLDER/monitoring_report_YYYYMMDD.pdf`` (if the env var
is set), otherwise the current working directory.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from meta_analytics.monitoring_report import generate_monitoring_report


def _parse_date(value: str | None, *, end_of_day: bool = False) -> datetime | None:
    if not value:
        return None
    try:
        d = datetime.strptime(value, "%Y-%m-%d")  # noqa: DTZ007
    except ValueError as exc:
        raise CommandError(f"Invalid date {value!r}, expected YYYY-MM-DD") from exc
    if end_of_day:
        d = d.replace(hour=23, minute=59)
    return d.replace(tzinfo=ZoneInfo("UTC"))


class Command(BaseCommand):
    help = "Generate the META3 monitoring report as a PDF."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            dest="output",
            default=None,
            help=(
                "Output PDF path (or folder). Defaults to "
                "$META_ANALYSIS_FOLDER/monitoring_report_YYYYMMDD.pdf if set, "
                "otherwise the current directory."
            ),
        )
        parser.add_argument(
            "--cutoff-date",
            dest="cutoff_date",
            default=None,
            help="Cutoff date (YYYY-MM-DD, UTC). Defaults to today.",
        )
        parser.add_argument(
            "--data-download-date",
            dest="data_download_date",
            default=None,
            help="Data download date (YYYY-MM-DD, UTC). Defaults to today.",
        )
        parser.add_argument(
            "--end-of-trial-date",
            dest="end_of_trial_date",
            default=None,
            help=(
                "End-of-trial date (YYYY-MM-DD, UTC). Used to bound the "
                "'future appointments' table. Defaults to cutoff_date."
            ),
        )
        parser.add_argument(
            "--verbose-pdf",
            dest="verbose_pdf",
            action="store_true",
            help="Print progress messages and enable tqdm progress bars.",
        )

    def handle(self, *args, **options):  # noqa: ARG002
        cutoff_date = _parse_date(options["cutoff_date"], end_of_day=True)
        data_download_date = _parse_date(options["data_download_date"])
        end_of_trial_date = _parse_date(options["end_of_trial_date"])

        if not end_of_trial_date:
            end_of_trial_date = settings.END_OF_TRAIL_DATETIME

        effective_cutoff = cutoff_date or datetime.now(tz=ZoneInfo("UTC")).replace(
            hour=23, minute=59, second=0, microsecond=0
        )
        filename = f"monitoring_report_{effective_cutoff.strftime('%Y%m%d')}.pdf"

        output_raw = options["output"]
        if output_raw:
            output_path = Path(output_raw).expanduser()
            if output_path.is_dir() or output_raw.endswith(os.sep):
                output_path = output_path / filename
        elif os.environ.get("META_ANALYSIS_FOLDER"):
            output_path = Path(os.environ["META_ANALYSIS_FOLDER"]).expanduser() / filename
        else:
            output_path = Path.cwd() / filename

        self.stdout.write(f"Generating monitoring report -> {output_path}")
        result = generate_monitoring_report(
            output_path=output_path,
            cutoff_date=cutoff_date,
            data_download_date=data_download_date,
            end_of_trial_date=end_of_trial_date,
            verbose=options["verbose_pdf"],
        )
        self.stdout.write(self.style.SUCCESS(f"Wrote {result}"))
        sys.stdout.flush()
