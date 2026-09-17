"""Encoding of stored values as AcroForm radio button export values.

A radio button's export value is written into the PDF as a *name* object.
reportlab does not escape the PDF name delimiters, so a stored value such
as ``N/A`` (``NOT_APPLICABLE``) would be written as ``/N`` and silently
truncated on read.

``encode_pdf_value`` maps a stored value to a name-safe token and
``decode_pdf_value`` maps it back, given the same choices tuple the form
was built from. A reader of a completed PDF must decode the radio values;
text fields are unaffected.
"""

from __future__ import annotations

import re

SAFE_CHARS = re.compile(r"[^A-Za-z0-9_.:@+-]")


def is_pdf_name_safe(value: str) -> bool:
    """Returns True if `value` survives a round trip through a PDF name."""
    value = str(value)
    return bool(value) and not SAFE_CHARS.search(value)


def encode_pdf_value(value: str) -> str:
    """Returns `value` with PDF name delimiters replaced by an underscore.

    For example, `N/A` is returned as `N_A`.
    """
    return SAFE_CHARS.sub("_", str(value))


def encode_choices(choices: tuple[tuple[str, str], ...]) -> tuple[tuple[str, str], ...]:
    """Returns `choices` with each stored value encoded for a PDF name.

    Raises if two stored values encode to the same token, since the
    completed form could then not be decoded.
    """
    encoded = tuple((encode_pdf_value(value), display) for value, display in choices)
    tokens = [token for token, _ in encoded]
    if len(set(tokens)) != len(tokens):
        raise ValueError(f"Choices do not encode uniquely for a PDF name. Got {choices}.")
    return encoded


def decode_pdf_value(token: str, choices: tuple[tuple[str, str], ...]) -> str:
    """Returns the stored value for a radio `token` read from a completed PDF.

    Returns an empty string if the field was left blank (`Off`) or the
    token does not match any of `choices`.
    """
    if not token or token in ("Off", "/Off"):
        return ""
    token = token.lstrip("/")
    for value, _ in choices:
        if encode_pdf_value(value) == token:
            return value
    return ""
