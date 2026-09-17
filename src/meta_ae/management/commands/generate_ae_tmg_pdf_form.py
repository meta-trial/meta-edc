"""Generate a writeable (AcroForm) AE TMG Report PDF for emailing to a TMG
investigator.

The form is built from an ``AeInitial``; no ``AeTmg`` row need exist. The
original AE report is reproduced as reference text and the investigator's
section is left blank and writeable. Field names match the ``AeTmg`` model
field names.

Each PDF is encrypted with its own generated password, printed here once.
Send the form and the password by different channels; the password is not
stored, so a lost one means regenerating the form.

Usage::

    uv run manage.py generate_ae_tmg_pdf_form --action-identifier=<identifier>
    uv run manage.py generate_ae_tmg_pdf_form --subject-identifier=<identifier>
    uv run manage.py generate_ae_tmg_pdf_form --subject-identifier=<identifier> \
        --path=/tmp/forms
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand, CommandError

from meta_ae.models import AeInitial
from meta_ae.pdf_forms import AeTmgPdfForm, generate_password


class Command(BaseCommand):
    help = "Generate a writeable AE TMG Report PDF from an AeInitial"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument(
            "--action-identifier",
            dest="action_identifier",
            default="",
            help="AeInitial action identifier. Generates one form.",
        )
        parser.add_argument(
            "--subject-identifier",
            dest="subject_identifier",
            default="",
            help="Subject identifier. Generates one form per AeInitial for the subject.",
        )
        parser.add_argument(
            "--path",
            dest="path",
            default=".",
            help="Folder to write the PDF(s) to. Defaults to the current folder.",
        )

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: ARG002
        queryset = self.get_queryset(options)
        path = Path(options["path"]).expanduser()
        for ae_initial in queryset:
            password = generate_password()
            pdf_path = AeTmgPdfForm(ae_initial).render(path, password=password)
            self.stdout.write(self.style.SUCCESS(f"Wrote {pdf_path}"))
            self.stdout.write(f"Password: {password}")
        self.stdout.write(
            self.style.WARNING(
                "Send each form and its password by different channels. The "
                "passwords are not stored anywhere."
            )
        )

    @staticmethod
    def get_queryset(options: dict[str, Any]) -> Any:
        """Returns the AeInitial queryset for the given options."""
        action_identifier = options["action_identifier"]
        subject_identifier = options["subject_identifier"]
        if not action_identifier and not subject_identifier:
            raise CommandError("Specify either --action-identifier or --subject-identifier.")
        if action_identifier and subject_identifier:
            raise CommandError(
                "Specify either --action-identifier or --subject-identifier, not both."
            )
        opts = (
            {"action_identifier": action_identifier}
            if action_identifier
            else {"subject_identifier": subject_identifier}
        )
        queryset = AeInitial.objects.filter(**opts).order_by("report_datetime")
        if not queryset.exists():
            raise CommandError(f"No AeInitial found. Got {opts}.")
        return queryset
