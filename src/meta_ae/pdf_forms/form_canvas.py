"""A thin layout wrapper over a reportlab canvas for building AcroForm PDFs.

The wrapper keeps a top-down cursor (``self.y``) and breaks pages on its
own, so callers describe the form top to bottom without tracking
coordinates. Every writeable widget is an AcroForm field, named by the
caller, so a completed PDF can be read back with ``pypdf``.
"""

from __future__ import annotations

from typing import BinaryIO

from reportlab.lib.colors import Color, black, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas as pdfgen_canvas

from .values import is_pdf_name_safe

FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_SIZE = 9
LEADING = 12.0

LEFT_MARGIN = 2.0 * cm
RIGHT_MARGIN = 2.0 * cm
TOP_MARGIN = 2.0 * cm
BOTTOM_MARGIN = 2.0 * cm

LABEL_WIDTH = 5.5 * cm

FIELD_BORDER = Color(0.45, 0.45, 0.45)
FIELD_FILL = Color(0.96, 0.96, 0.99)
BAND_FILL = Color(0.88, 0.88, 0.90)
HEADER_COLOR = Color(0.60, 0.10, 0.10)
MUTED = Color(0.35, 0.35, 0.35)


class FormCanvas:
    """Draws labelled read-only text and AcroForm widgets top to bottom."""

    pagesize = A4

    def __init__(self, target: str | BinaryIO, title: str = "", subject: str = "") -> None:
        """`target` is a path or an open binary stream, e.g. a `BytesIO`.

        Every text argument is coerced with `str()` on the way to
        reportlab, which cannot render Django lazy translation objects
        such as a model field's `verbose_name`.
        """
        self.canvas = pdfgen_canvas.Canvas(target, pagesize=self.pagesize)
        self.canvas.setTitle(str(title))
        self.canvas.setSubject(str(subject))
        self.canvas.setAuthor("META Trial EDC")
        self.page_width, self.page_height = self.pagesize
        self.content_width = self.page_width - LEFT_MARGIN - RIGHT_MARGIN
        self.page_number = 0
        self.y = 0.0
        self.header_text = ""
        self.footer_text = ""
        self.footer_subtext = ""
        self._start_page()

    # page handling -----------------------------------------------------
    def _start_page(self) -> None:
        if self.page_number:
            self.canvas.showPage()
        self.page_number += 1
        self.y = self.page_height - TOP_MARGIN

    def _require(self, height: float) -> None:
        """Breaks to a new page when ``height`` will not fit below the cursor."""
        if self.y - height < BOTTOM_MARGIN:
            self._finish_page()
            self._start_page()

    def _finish_page(self) -> None:
        """Draws the running header and footer on the page being left.

        Drawn on leaving the page, not on starting it, so that the caller
        may set `header_text` and the footer attributes after the canvas
        is constructed and still have them appear on the first page.
        """
        self._draw_header()
        self._draw_footer()

    def _draw_header(self) -> None:
        """Draws `header_text` in the top margin of every page."""
        if not self.header_text:
            return
        header_text = str(self.header_text)
        y = self.page_height - TOP_MARGIN + 0.55 * cm
        self.canvas.setFont(FONT_BOLD, 8)
        self.canvas.setFillColor(HEADER_COLOR)
        self.canvas.drawString(LEFT_MARGIN, y, header_text)
        self.canvas.drawRightString(self.page_width - RIGHT_MARGIN, y, header_text)
        self.canvas.setStrokeColor(BAND_FILL)
        self.canvas.setLineWidth(0.5)
        self.canvas.line(
            LEFT_MARGIN, y - 0.18 * cm, self.page_width - RIGHT_MARGIN, y - 0.18 * cm
        )
        self.canvas.setFillColor(black)

    def _draw_footer(self) -> None:
        """Draws `footer_text` and `footer_subtext` on every page."""
        y = BOTTOM_MARGIN - 0.7 * cm
        self.canvas.setFont(FONT, 7)
        self.canvas.setFillColor(black)
        self.canvas.drawString(LEFT_MARGIN, y, str(self.footer_text))
        self.canvas.drawRightString(
            self.page_width - RIGHT_MARGIN, y, f"Page {self.page_number}"
        )
        if self.footer_subtext:
            self.canvas.setFillColor(MUTED)
            self.canvas.drawString(LEFT_MARGIN, y - 9.0, str(self.footer_subtext))
            self.canvas.setFillColor(black)

    def save(self) -> None:
        self._finish_page()
        self.canvas.save()

    # static text -------------------------------------------------------
    def spacer(self, height: float = 0.35 * cm) -> None:
        self.y -= height

    def title(self, text: str, size: int = 14) -> None:
        text = str(text)
        self._require(size + 0.4 * cm)
        self.canvas.setFont(FONT_BOLD, size)
        self.canvas.setFillColor(black)
        self.canvas.drawString(LEFT_MARGIN, self.y - size, text)
        self.y -= size + 0.25 * cm

    def band(self, text: str) -> None:
        """Draws a full width section heading on a grey band."""
        text = str(text)
        height = 0.62 * cm
        self._require(height + 0.3 * cm)
        self.canvas.setFillColor(BAND_FILL)
        self.canvas.rect(
            LEFT_MARGIN, self.y - height, self.content_width, height, stroke=0, fill=1
        )
        self.canvas.setFillColor(black)
        self.canvas.setFont(FONT_BOLD, 10)
        self.canvas.drawString(LEFT_MARGIN + 0.15 * cm, self.y - height + 0.18 * cm, text)
        self.y -= height + 0.25 * cm

    def note(self, text: str) -> None:
        lines = simpleSplit(str(text), FONT, 8, self.content_width)
        self._require(len(lines) * 10.0)
        self.canvas.setFont(FONT, 8)
        self.canvas.setFillColor(MUTED)
        for line in lines:
            self.canvas.drawString(LEFT_MARGIN, self.y - 8, line)
            self.y -= 10.0
        self.canvas.setFillColor(black)
        self.y -= 0.15 * cm

    def readonly_row(self, label: str, value: str) -> None:
        """Draws a label/value pair as plain text, wrapping the value."""
        label = str(label)
        value_width = self.content_width - LABEL_WIDTH
        lines = simpleSplit(str(value or "--"), FONT, FONT_SIZE, value_width) or ["--"]
        self._require(len(lines) * LEADING + 0.1 * cm)
        self.canvas.setFillColor(black)
        self.canvas.setFont(FONT_BOLD, FONT_SIZE)
        self.canvas.drawString(LEFT_MARGIN, self.y - FONT_SIZE, label)
        self.canvas.setFont(FONT, FONT_SIZE)
        for index, line in enumerate(lines):
            self.canvas.drawString(
                LEFT_MARGIN + LABEL_WIDTH, self.y - FONT_SIZE - index * LEADING, line
            )
        self.y -= len(lines) * LEADING + 0.1 * cm

    def _label(self, text: str) -> None:
        lines = simpleSplit(str(text), FONT_BOLD, FONT_SIZE, self.content_width)
        self._require(len(lines) * LEADING)
        self.canvas.setFont(FONT_BOLD, FONT_SIZE)
        self.canvas.setFillColor(black)
        for line in lines:
            self.canvas.drawString(LEFT_MARGIN, self.y - FONT_SIZE, line)
            self.y -= LEADING
        self.y -= 0.08 * cm

    # form fields -------------------------------------------------------
    def textfield(  # noqa: PLR0913
        self,
        name: str,
        label: str,
        tooltip: str = "",
        width: float | None = None,
        lines: int = 1,
        value: str = "",
    ) -> None:
        """Adds a single or multi line AcroForm text field named ``name``."""
        label, tooltip, value = str(label), str(tooltip), str(value)
        height = 0.62 * cm if lines == 1 else lines * 0.44 * cm
        self._label(label)
        self._require(height + 0.3 * cm)
        self.canvas.acroForm.textfield(
            name=name,
            tooltip=tooltip or label,
            value=value,
            x=LEFT_MARGIN,
            y=self.y - height,
            width=width or self.content_width,
            height=height,
            fontName=FONT,
            fontSize=FONT_SIZE,
            textColor=black,
            fillColor=FIELD_FILL,
            borderColor=FIELD_BORDER,
            borderWidth=0.5,
            borderStyle="inset",
            forceBorder=True,
            fieldFlags="multiline" if lines > 1 else "",
        )
        self.y -= height + 0.3 * cm

    def radio_group(
        self,
        name: str,
        label: str,
        choices: tuple[tuple[str, str], ...],
        tooltip: str = "",
    ) -> None:
        """Adds one AcroForm radio group named ``name``.

        Each option exports its own ``value``, so a returned PDF yields the
        stored choice (e.g. ``Yes``) rather than the displayed label. Values
        must already be PDF name safe, see ``values.encode_choices``.
        """
        label, tooltip = str(label), str(tooltip)
        choices = tuple((str(value), str(display)) for value, display in choices)
        for value, _ in choices:
            if not is_pdf_name_safe(value):
                raise ValueError(
                    f"Radio value is not PDF name safe. Pass it through "
                    f"`encode_choices` first. Got {name}={value!r}."
                )
        self._label(label)
        size = 11
        for value, display in choices:
            lines = simpleSplit(display, FONT, FONT_SIZE, self.content_width - 1.0 * cm)
            height = max(size + 4, len(lines) * LEADING)
            self._require(height)
            self.canvas.acroForm.radio(
                name=name,
                tooltip=tooltip or f"{label} [{value}]",
                value=value,
                selected=False,
                x=LEFT_MARGIN + 0.1 * cm,
                y=self.y - size - 2,
                size=size,
                buttonStyle="circle",
                shape="circle",
                borderColor=FIELD_BORDER,
                fillColor=white,
                borderWidth=0.7,
                # forceBorder would draw a second, offset circle over the widget's
                # own appearance stream.
                forceBorder=False,
            )
            self.canvas.setFont(FONT, FONT_SIZE)
            self.canvas.setFillColor(black)
            for index, line in enumerate(lines):
                self.canvas.drawString(
                    LEFT_MARGIN + 0.75 * cm,
                    self.y - FONT_SIZE - 2 - index * LEADING,
                    line,
                )
            self.y -= height
        self.y -= 0.25 * cm

    def signature_row(self, name_field: str, date_field: str) -> None:
        """Adds a name/date pair for the wet signature block."""
        height = 0.62 * cm
        width = (self.content_width - 1.0 * cm) / 2
        self._require(height + 0.8 * cm)
        for index, (field, label) in enumerate(
            ((name_field, "Name (print)"), (date_field, "Date (YYYY-MM-DD)"))
        ):
            x = LEFT_MARGIN + index * (width + 1.0 * cm)
            self.canvas.setFont(FONT_BOLD, FONT_SIZE)
            self.canvas.setFillColor(black)
            self.canvas.drawString(x, self.y - FONT_SIZE, label)
            self.canvas.acroForm.textfield(
                name=field,
                tooltip=label,
                x=x,
                y=self.y - FONT_SIZE - height - 0.1 * cm,
                width=width,
                height=height,
                fontName=FONT,
                fontSize=FONT_SIZE,
                textColor=black,
                fillColor=FIELD_FILL,
                borderColor=FIELD_BORDER,
                borderWidth=0.5,
                borderStyle="inset",
                forceBorder=True,
            )
        self.y -= FONT_SIZE + height + 0.5 * cm
