"""Builds a writeable (AcroForm) PDF of the AE TMG Report.

The form is generated from an ``AeInitial``; no ``AeTmg`` row need exist.
The original report is drawn as static text for reference and the TMG
investigator's section is left blank and writeable.

Every writeable field is named after its ``AeTmg`` model field, so a
completed PDF can be read back with ``pypdf`` and used to populate the
model. The two signature fields are not model fields and are prefixed
``signature_``.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any

from clinicedc_constants import OTHER
from clinicedc_constants.choices import YES_NO
from django.utils import timezone
from edc_adverse_event.models import AeClassification
from edc_adverse_event.utils import get_ae_model
from edc_model.choices import REPORT_STATUS
from edc_protocol.trial_settings import trial_settings
from edc_utils import formatted_date, formatted_datetime
from reportlab.lib.units import cm

from .encryption import encrypt_pdf
from .form_canvas import FormCanvas
from .values import encode_choices

if TYPE_CHECKING:
    from meta_ae.models import AeInitial

DATETIME_HINT = "YYYY-MM-DD HH:MM"

#: Width of the single line date fields, in points.
DATE_FIELD_WIDTH = 7.0 * cm

DISTRIBUTION = "meta-edc"

#: Writeable fields, in the order of the `Investigator's section` admin fieldset.
INVESTIGATOR_FIELDS = (
    "ae_received_datetime",
    "clinical_review_datetime",
    "investigator_comments",
    "original_report_agreed",
    "investigator_narrative",
    "investigator_ae_classification",
    "investigator_ae_classification_other",
    "officials_notified",
    "report_status",
    "report_closed_datetime",
)


def get_revision() -> str:
    """Returns the installed `meta-edc` version, that is, the pyproject version.

    Returns an empty string if the distribution metadata is not installed,
    for example when running from a source checkout that was never installed.
    """
    try:
        return version(DISTRIBUTION)
    except PackageNotFoundError:
        return ""


def get_ae_classification_choices() -> tuple[tuple[str, str], ...]:
    """Returns AeClassification `name`/`display_name` pairs for the radio group.

    The stored value is `name`, which is what an importer would pass to
    `AeClassification.objects.get(name=...)` after `decode_pdf_value`.
    """
    return tuple(
        (obj.name, obj.display_name)
        for obj in AeClassification.objects.all().order_by("display_name")
    )


class AeTmgPdfForm:
    """Renders the AE TMG Report as a fillable PDF for one `AeInitial`."""

    canvas_cls = FormCanvas
    header_text = "CONFIDENTIAL"
    instructions = (
        "Confidential. For completion by TMG Investigators only. Complete the "
        "investigator's section below, save the file and return it by email. "
        "Section 1 reproduces the original AE report and is for reference only."
    )

    def __init__(self, ae_initial: AeInitial) -> None:
        self.ae_initial = ae_initial

    @property
    def revision(self) -> str:
        return get_revision()

    @staticmethod
    def get_field(field_name: str) -> Any:
        """Returns the named field from the AeTmg model."""
        return get_ae_model("aetmg")._meta.get_field(field_name)

    @classmethod
    def get_field_label(cls, field_name: str, hint: str = "") -> str:
        """Returns the AeTmg field's `verbose_name` as the label for the PDF.

        A `verbose_name` (and a `help_text` passed in as `hint`) may be a
        Django lazy translation object. reportlab cannot render one, so it
        is resolved here rather than at the point it is drawn. Labels are
        taken from the model so the PDF tracks it, rather than restating
        the wording in two places.
        """
        label = str(cls.get_field(field_name).verbose_name).strip()
        if label.endswith("?"):
            return label
        label = label.rstrip(":.").strip()
        if hint:
            label = f"{label} ({str(hint).strip().rstrip('.')})"
        return f"{label}:"

    @classmethod
    def get_field_help_text(cls, field_name: str) -> str:
        """Returns the AeTmg field's `help_text`, resolved if it is lazy."""
        return str(cls.get_field(field_name).help_text or "").strip()

    @property
    def study_title(self) -> str:
        return trial_settings.project_name

    @property
    def filename(self) -> str:
        return (
            f"ae_tmg_report_{self.ae_initial.subject_identifier}_"
            f"{self.ae_initial.action_identifier[-9:]}.pdf"
        )

    @property
    def ae_classification_display(self) -> str:
        """Returns the original AE classification, appending `other` if given."""
        try:
            display = self.ae_initial.ae_classification.display_name
            name = self.ae_initial.ae_classification.name
        except AttributeError:
            return "--"
        if name == OTHER and self.ae_initial.ae_classification_other:
            return f"{display}: {self.ae_initial.ae_classification_other.rstrip()}"
        return display

    def render(self, path: str | Path, password: str = "") -> Path:
        """Writes the PDF to `path` and returns the path.

        If `path` is a directory, `self.filename` is used inside it. If
        `password` is given the file is encrypted with it; the document is
        built in memory, so the unencrypted PDF is never written to disk.
        """
        path = Path(path)
        if path.is_dir():
            path = path / self.filename
        path.parent.mkdir(parents=True, exist_ok=True)
        buffer = BytesIO()
        doc = self.canvas_cls(
            buffer,
            title=f"AE TMG Report: {self.ae_initial.subject_identifier}",
            subject=f"AE Initial {self.ae_initial.action_identifier}",
        )
        doc.footer_text = (
            f"{self.study_title} | AE TMG Report | "
            f"{self.ae_initial.subject_identifier} | "
            f"AE Initial {self.ae_initial.action_identifier}"
        )
        doc.header_text = self.header_text
        doc.footer_subtext = self.get_footer_subtext()
        self.draw_header(doc)
        self.draw_original_report(doc)
        self.draw_investigator_section(doc)
        self.draw_signature(doc)
        doc.save()
        if password:
            return encrypt_pdf(buffer, path, password)
        path.write_bytes(buffer.getvalue())
        return path

    def get_footer_subtext(self) -> str:
        """Returns the `meta-edc` revision and the date this form was generated."""
        generated = formatted_date(timezone.localdate())
        revision = f"{DISTRIBUTION} {self.revision}" if self.revision else DISTRIBUTION
        return f"{revision} | Generated {generated}"

    def draw_header(self, doc: FormCanvas) -> None:
        doc.title(f"{self.study_title}: AE TMG Report")
        doc.note(self.instructions)
        doc.spacer()

    def draw_original_report(self, doc: FormCanvas) -> None:
        ae_initial = self.ae_initial
        doc.band("Section 1: Original AE report (reference only)")
        doc.readonly_row("Subject identifier:", ae_initial.subject_identifier)
        doc.readonly_row(
            "Study site:", f"{ae_initial.site.id}: {ae_initial.site.name.title()}"
        )
        doc.readonly_row("AE Initial reference:", ae_initial.action_identifier)
        doc.readonly_row(
            "Report date/time:", formatted_datetime(ae_initial.report_datetime) or "--"
        )
        doc.readonly_row(
            "AE awareness date:", formatted_date(ae_initial.ae_awareness_date) or "--"
        )
        doc.readonly_row("AE start date:", formatted_date(ae_initial.ae_start_date) or "--")
        doc.readonly_row("Severity of AE:", ae_initial.get_ae_grade_display())
        doc.readonly_row(
            "Relation to study drug:", ae_initial.get_study_drug_relation_display() or "--"
        )
        doc.readonly_row("AE classification:", self.ae_classification_display)
        doc.readonly_row("AE description:", ae_initial.ae_description)
        doc.spacer()

    def draw_investigator_section(self, doc: FormCanvas) -> None:
        doc.band("Section 2: Investigator's section")
        doc.textfield(
            "ae_received_datetime",
            self.get_field_label("ae_received_datetime", hint=DATETIME_HINT),
            tooltip=DATETIME_HINT,
            width=DATE_FIELD_WIDTH,
        )
        doc.textfield(
            "clinical_review_datetime",
            self.get_field_label("clinical_review_datetime", hint=DATETIME_HINT),
            tooltip=DATETIME_HINT,
            width=DATE_FIELD_WIDTH,
        )
        doc.textfield(
            "investigator_comments",
            self.get_field_label("investigator_comments"),
            lines=5,
        )
        doc.radio_group(
            "original_report_agreed",
            self.get_field_label("original_report_agreed"),
            encode_choices(YES_NO),
        )
        doc.textfield(
            "investigator_narrative",
            self.get_field_label(
                "investigator_narrative",
                hint="if you do not agree with the original report, explain here",
            ),
            lines=8,
        )
        doc.radio_group(
            "investigator_ae_classification",
            self.get_field_label(
                "investigator_ae_classification",
                hint=self.get_field_help_text("investigator_ae_classification"),
            ),
            encode_choices(get_ae_classification_choices()),
        )
        doc.textfield(
            "investigator_ae_classification_other",
            self.get_field_label("investigator_ae_classification_other"),
        )
        doc.textfield(
            "officials_notified",
            self.get_field_label("officials_notified", hint=DATETIME_HINT),
            tooltip=DATETIME_HINT,
            width=DATE_FIELD_WIDTH,
        )
        doc.radio_group(
            "report_status",
            self.get_field_label("report_status"),
            encode_choices(tuple(REPORT_STATUS)),
        )
        doc.textfield(
            "report_closed_datetime",
            self.get_field_label("report_closed_datetime", hint=DATETIME_HINT),
            tooltip=DATETIME_HINT,
            width=DATE_FIELD_WIDTH,
        )

    def draw_signature(self, doc: FormCanvas) -> None:
        doc.band("Section 3: TMG investigator")
        doc.signature_row("signature_name", "signature_date")
        doc.note(
            "Return the completed file by email to the trial coordinator. Keep the "
            "field values as typed; do not flatten or print/rescan the form. This "
            "file is password protected; do not send the password with the file."
        )


def render_ae_tmg_pdf_form(
    ae_initial: AeInitial, path: str | Path, password: str = ""
) -> Path:
    """Renders the AE TMG fillable PDF for `ae_initial` and returns the path."""
    return AeTmgPdfForm(ae_initial).render(path, password=password)
