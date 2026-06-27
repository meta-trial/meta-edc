"""Generate blank, printable *HIV Exit Review* forms as a single PDF.

One A4 page is produced per subject listed on the
``meta_reports.HivExitReviewReport`` view (subjects still missing the
``meta_subject.hivexitreview`` CRF). Each page mirrors the online CRF but leaves
blank lines/boxes for hand-written entries, with name/date/signature lines at
the foot of the form.

Usage::

    uv run manage.py generate_hiv_exit_review_forms \\
        --output /path/to/hiv_exit_review_forms.pdf

The ``--output`` path may be a file or a directory; if a directory (or omitted)
the filename ``hiv_exit_review_forms.pdf`` is used. ``--site`` and ``--subject``
restrict the subjects included.

The PDF contains PII and is always AES-256 encrypted. The command prompts for
the password (and a confirmation) on the CLI. For non-interactive runs, set the
password in an environment variable and pass its name via ``--password-env``.
"""

from __future__ import annotations

import os
import sys
from getpass import getpass
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from meta_reports.hiv_exit_review_form_report import (
    FontNotFoundError,
    PageOverflowError,
    generate_hiv_exit_review_forms,
)
from meta_reports.models import HivExitReviewReport


class Command(BaseCommand):
    help = "Generate blank HIV Exit Review forms (one page per subject) as a PDF."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            dest="output",
            default=None,
            help=(
                "Output PDF path or folder. Defaults to "
                "hiv_exit_review_forms.pdf in the current directory."
            ),
        )
        parser.add_argument(
            "--site",
            dest="site_id",
            type=int,
            default=None,
            help="Restrict to a single site id.",
        )
        parser.add_argument(
            "--subject",
            dest="subject_identifier",
            default=None,
            help="Restrict to a single subject identifier.",
        )
        parser.add_argument(
            "--password-env",
            dest="password_env",
            default=None,
            help=(
                "Name of an environment variable holding the PDF password "
                "(non-interactive). If omitted, you are prompted on the CLI."
            ),
        )

    def get_password(self, options) -> str:
        if options["password_env"]:
            password = os.environ.get(options["password_env"])
            if not password:
                raise CommandError(
                    f"Environment variable {options['password_env']!r} is not set or empty."
                )
            return password
        password = getpass("Enter a password to protect the PDF: ")
        if not password:
            raise CommandError("A password is required.")
        if password != getpass("Confirm password: "):
            raise CommandError("Passwords do not match.")
        return password

    def handle(self, *args, **options):  # noqa: ARG002
        output = Path(options["output"]).expanduser() if options["output"] else Path.cwd()
        password = self.get_password(options)

        queryset = HivExitReviewReport.objects.all().order_by("site", "subject_identifier")
        if options["site_id"]:
            queryset = queryset.filter(site_id=options["site_id"])
        if options["subject_identifier"]:
            queryset = queryset.filter(subject_identifier=options["subject_identifier"])

        count = queryset.count()
        self.stdout.write(f"Generating HIV Exit Review forms for {count} subject(s) ...")
        try:
            written = generate_hiv_exit_review_forms(
                output_path=output, queryset=queryset, password=password
            )
        except FontNotFoundError as exc:
            raise CommandError(
                f"{exc}\n\nThe form embeds Liberation Sans for consistent, single-page "
                "output. The font files ship under meta_reports/fonts/ — ensure they "
                "were deployed with the package. As a fallback you can install the font "
                "system-wide:\n    sudo apt-get install fonts-liberation"
            ) from exc
        except PageOverflowError as exc:
            raise CommandError(
                f"{exc}\n\nThis usually means a system font is being substituted for the "
                "embedded one. Verify the bundled fonts under meta_reports/fonts/ are "
                "present, or install them system-wide:\n"
                "    sudo apt-get install fonts-liberation"
            ) from exc
        self.stdout.write(self.style.SUCCESS(f"Wrote {written} (password-protected)"))
        sys.stdout.flush()
