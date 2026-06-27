"""Generate a printable, blank *HIV Exit Review* form for each subject who is
still missing the CRF.

The subjects are drawn from the unmanaged report view
``meta_reports.HivExitReviewReport`` (subjects without a submitted
``meta_subject.hivexitreview`` CRF). One A4 page is produced per subject and the
pages are concatenated into a single PDF.

The layout mirrors the online ``HivExitReview`` CRF but leaves blank lines and
boxes for hand-written entries, and ends with name/date/signature lines for the
person who completes the form by hand.
"""

from __future__ import annotations

import io
from html import escape
from pathlib import Path
from typing import TYPE_CHECKING

from pypdf import PdfReader, PdfWriter
from weasyprint import HTML

from .models import HivExitReviewReport

if TYPE_CHECKING:
    from django.db.models import QuerySet

__all__ = ["generate_hiv_exit_review_forms"]

# A blank line for a short, single-line hand-written answer.
_LINE = '<span class="fill"></span>'


def _page_style() -> str:
    return """
<style>
  @page {
    size: A4;
    margin: 18mm 14mm 18mm 14mm;
    @top-center {
      content: "META Trial: CONFIDENTIAL";
      font-size: 8pt;
      font-weight: bold;
      color: #444;
    }
    @bottom-center {
      content: "META Trial: CONFIDENTIAL";
      font-size: 8pt;
      font-weight: bold;
      color: #444;
    }
    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
      font-size: 8pt;
      color: #666;
    }
  }
  body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10pt;
    color: #000;
  }
  .subject-page {
    page-break-after: always;
  }
  .subject-page:last-child {
    page-break-after: auto;
  }
  .form-title {
    font-size: 13pt;
    font-weight: bold;
    margin: 0 0 6px 0;
  }
  table.header {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 10px;
  }
  table.header td {
    border: 1px solid #000;
    padding: 5px 7px;
    font-size: 10pt;
  }
  table.header td.label {
    font-weight: bold;
    width: 26%;
    background: #f0f0f0;
  }
  .section-header {
    background: #222;
    color: #fff;
    font-weight: bold;
    padding: 4px 7px;
    margin: 12px 0 0 0;
    font-size: 10.5pt;
  }
  table.fields {
    width: 100%;
    border-collapse: collapse;
  }
  table.fields td {
    padding: 7px 6px;
    vertical-align: top;
    border-bottom: 1px solid #ccc;
  }
  table.fields.arvs td {
    padding-top: 12px;
    padding-bottom: 12px;
  }
  table.fields td.q {
    width: 56%;
  }
  table.fields td.q.full {
    width: auto;
  }
  table.fields td.q .qnum {
    font-weight: bold;
    text-decoration: underline;
  }
  td.a {
    width: 44%;
  }
  .units {
    color: #555;
    font-size: 9pt;
  }
  .note {
    color: #555;
    font-size: 8.5pt;
    font-style: italic;
  }
  .fill {
    display: inline-block;
    border-bottom: 1px solid #000;
    min-width: 150px;
    height: 1.1em;
  }
  .fill.short {
    min-width: 90px;
  }
  .answer-box {
    border: 1px solid #000;
    height: 70px;
    width: 100%;
    margin-top: 6px;
  }
  .answer-box.tall {
    height: 100px;
  }
  .checkbox {
    display: inline-block;
    width: 11px;
    height: 11px;
    border: 1px solid #000;
    margin-right: 4px;
    vertical-align: middle;
  }
  .opt {
    margin-right: 18px;
    white-space: nowrap;
  }
  table.signature {
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
  }
  table.signature td {
    padding: 14px 8px 4px 8px;
    border-bottom: 1px solid #000;
    font-size: 9pt;
    color: #333;
    vertical-align: bottom;
  }
  table.signature tr.captions td {
    border-bottom: none;
    padding: 2px 8px 0 8px;
  }
  .office-use {
    border: 1.5px solid #000;
    margin-top: 22px;
    padding: 6px 10px 12px 10px;
  }
  .office-use .office-title {
    font-weight: bold;
    font-size: 10pt;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
  }
  .office-use .office-sub {
    font-size: 8.5pt;
    color: #555;
    font-style: italic;
    margin-bottom: 6px;
  }
</style>
"""


def _header_box(obj: HivExitReviewReport) -> str:
    site = ""
    if obj.site_id:
        site = f"{obj.site_id}: {escape(obj.site.name.title())}"
    return f"""
<table class="header">
  <tr>
    <td class="label">Subject identifier</td><td>{escape(obj.subject_identifier or "")}</td>
    <td class="label">Site</td><td>{site}</td>
  </tr>
  <tr>
    <td class="label">Initials</td><td>{escape(obj.initials or "")}</td>
    <td class="label">Hospital identifier</td><td>{escape(obj.hospital_identifier or "")}</td>
  </tr>
</table>
"""


def _form_body() -> str:
    """Blank form fields mirroring the HivExitReview CRF (static for every subject)."""
    return f"""
<table class="fields">
  <tr>
    <td class="q"><span class="qnum">1.</span> Report date</td>
    <td class="a">Date: {_LINE.replace("fill", "fill short")} &nbsp;&nbsp;
        Time: {_LINE.replace("fill", "fill short")}</td>
  </tr>
  <tr>
    <td class="q"><span class="qnum">2.</span> Are HIV test result and treatment
        information available?</td>
    <td class="a">
      <span class="opt"><span class="checkbox"></span>Yes</span>
      <span class="opt"><span class="checkbox"></span>No</span>
      <span class="opt"><span class="checkbox"></span>Pending</span>
    </td>
  </tr>
  <tr>
    <td class="q full" colspan="2">
      <span class="qnum">3.</span> If not available, please explain &hellip;
      <div class="answer-box"></div>
    </td>
  </tr>
</table>

<p class="section-header">HIV and ARVs</p>
<table class="fields arvs">
  <tr>
    <td class="q"><span class="qnum">4.</span> Last viral load</td>
    <td class="a">{_LINE} <span class="units">copies/mL</span></td>
  </tr>
  <tr>
    <td class="q"><span class="qnum">5.</span> Date of last viral load</td>
    <td class="a">{_LINE}</td>
  </tr>
  <tr>
    <td class="q"><span class="qnum">6.</span> Last CD4</td>
    <td class="a">{_LINE} <span class="units">cells/mm<sup>3</sup></span></td>
  </tr>
  <tr>
    <td class="q"><span class="qnum">7.</span> Date of last CD4</td>
    <td class="a">{_LINE}</td>
  </tr>
  <tr>
    <td class="q"><span class="qnum">8.</span> Which antiretroviral therapy regimen is
        the patient currently on?</td>
    <td class="a">{_LINE}</td>
  </tr>
  <tr>
    <td class="q"><span class="qnum">9.</span> If other, please specify</td>
    <td class="a">{_LINE}</td>
  </tr>
  <tr>
    <td class="q"><span class="qnum">10.</span> When did the patient start this current
        antiretroviral therapy regimen?</td>
    <td class="a">{_LINE}</td>
  </tr>
</table>

<p class="section-header">Comment</p>
<table class="fields">
  <tr>
    <td class="q full" colspan="2">
      <span class="qnum">11.</span> Any other comment?
      <span class="note">May be left blank.</span>
      <div class="answer-box tall"></div>
    </td>
  </tr>
</table>
"""


def _signature_block() -> str:
    return """
<table class="signature">
  <tr>
    <td style="width:45%">&nbsp;</td>
    <td style="width:25%">&nbsp;</td>
    <td style="width:30%">&nbsp;</td>
  </tr>
  <tr class="captions">
    <td>Name of person completing the form</td>
    <td>Date</td>
    <td>Signature</td>
  </tr>
</table>

<div class="office-use">
  <div class="office-title">FOR OFFICE USE ONLY</div>
  <div class="office-sub">To be completed by the person who transcribed this data into the
    EDC.</div>
  <table class="signature">
    <tr>
      <td style="width:45%">&nbsp;</td>
      <td style="width:25%">&nbsp;</td>
      <td style="width:30%">&nbsp;</td>
    </tr>
    <tr class="captions">
      <td>Name of person who transcribed into EDC</td>
      <td>Date</td>
      <td>Signature</td>
    </tr>
  </table>
</div>
"""


def _render_page(obj: HivExitReviewReport) -> str:
    return (
        '<div class="subject-page">'
        '<p class="form-title">HIV Exit Review</p>'
        f"{_header_box(obj)}"
        f"{_form_body()}"
        f"{_signature_block()}"
        "</div>"
    )


def _encrypt(pdf_bytes: bytes, password: str) -> bytes:
    """Return AES-256 encrypted PDF bytes requiring ``password`` to open."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.encrypt(user_password=password, algorithm="AES-256")
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def generate_hiv_exit_review_forms(
    output_path: str | Path,
    queryset: QuerySet[HivExitReviewReport] | None = None,
    password: str | None = None,
) -> Path:
    """Render a single combined PDF, one blank form page per subject.

    :param output_path: file path or directory for the PDF. If a directory, the
        filename ``hiv_exit_review_forms.pdf`` is used.
    :param queryset: optional pre-filtered queryset of ``HivExitReviewReport``.
        Defaults to all rows, ordered by site then subject_identifier.
    :param password: if given, the PDF is AES-256 encrypted and requires this
        password to open. The form contains PII, so a password is recommended.
    :returns: the path to the written PDF.
    """
    output_path = Path(output_path).expanduser()
    if output_path.is_dir() or str(output_path).endswith("/"):
        output_path = output_path / "hiv_exit_review_forms.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if queryset is None:
        queryset = HivExitReviewReport.objects.all().order_by("site", "subject_identifier")

    pages = [_render_page(obj) for obj in queryset]
    body = "".join(pages) if pages else "<p>No subjects without an HIV Exit Review form.</p>"

    raw_html = (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        f"{_page_style()}\n</head>\n<body>\n{body}\n</body>\n</html>\n"
    )
    pdf_bytes = HTML(string=raw_html).write_pdf()
    if password:
        pdf_bytes = _encrypt(pdf_bytes, password)
    output_path.write_bytes(pdf_bytes)
    return output_path
