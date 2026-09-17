"""Password protection for the generated PDF forms.

The PDF is encrypted with AES-256 by `pypdf`, which `clinicedc` already
depends on. reportlab's own encryption is not used: without the optional
`pyaes` package it can only manage RC4, which is deprecated and which
reportlab itself documents as very weak.

The same password is used for the user (open) and owner roles and all
permissions are granted, so the investigator needs one secret and the
form stays fillable and printable once open.
"""

from __future__ import annotations

import secrets
from io import BytesIO
from math import log2
from pathlib import Path

from pypdf import PdfWriter

ALGORITHM = "AES-256"

DIGITS = 4

#: Short, unambiguous words, chosen so a password can be read out over the
#: phone. Keep the list a power of two so the entropy is easy to state.
WORDS = (
    "amber",
    "anchor",
    "apple",
    "arrow",
    "aspen",
    "atlas",
    "autumn",
    "bacon",
    "badge",
    "basil",
    "beacon",
    "bison",
    "blend",
    "bloom",
    "brass",
    "bridge",
    "bronze",
    "brush",
    "cabin",
    "cable",
    "cactus",
    "camel",
    "candle",
    "canyon",
    "cargo",
    "carpet",
    "cedar",
    "chalk",
    "cherry",
    "cinder",
    "cloud",
    "clover",
    "cobalt",
    "comet",
    "copper",
    "coral",
    "cotton",
    "cove",
    "crane",
    "crest",
    "crown",
    "crystal",
    "dahlia",
    "daisy",
    "dapple",
    "dawn",
    "delta",
    "denim",
    "dial",
    "dolphin",
    "domino",
    "drift",
    "dune",
    "eagle",
    "ember",
    "emerald",
    "falcon",
    "fern",
    "fiddle",
    "flint",
    "forest",
    "fossil",
    "galaxy",
    "garnet",
    "gecko",
    "ginger",
    "glacier",
    "granite",
    "gravel",
    "harbor",
    "hazel",
    "heron",
    "hickory",
    "indigo",
    "island",
    "ivory",
    "jasmine",
    "jasper",
    "jungle",
    "kettle",
    "lagoon",
    "lantern",
    "latch",
    "laurel",
    "ledge",
    "lemon",
    "lichen",
    "lilac",
    "linen",
    "lotus",
    "lumber",
    "magnet",
    "mango",
    "maple",
    "marble",
    "meadow",
    "mesa",
    "millet",
    "mirror",
    "mosaic",
    "nectar",
    "nickel",
    "nutmeg",
    "oasis",
    "olive",
    "onyx",
    "orbit",
    "orchid",
    "osprey",
    "otter",
    "paddle",
    "pebble",
    "pepper",
    "pewter",
    "pigment",
    "pilot",
    "pine",
    "pivot",
    "plume",
    "pollen",
    "poplar",
    "prairie",
    "prism",
    "quarry",
    "quartz",
    "quiver",
    "radish",
    "raft",
)


def get_entropy_bits(word_count: int = 4, digits: int = DIGITS) -> float:
    """Returns the entropy of a generated password, in bits."""
    return word_count * log2(len(WORDS)) + digits * log2(10)


def generate_password(word_count: int = 4, digits: int = DIGITS) -> str:
    """Returns a readable password, for example `latch-quartz-ember-pine-7241`.

    The default is four words from a 128 word list plus four digits, about
    41 bits of entropy. That is a deliberate trade for a password that can
    be read out over the phone; raise `word_count` where the form is going
    somewhere that warrants it.
    """
    if word_count < 1:
        raise ValueError(f"Expected at least one word. Got {word_count}.")
    words = [secrets.choice(WORDS) for _ in range(word_count)]
    if digits:
        words.append("".join(str(secrets.randbelow(10)) for _ in range(digits)))
    return "-".join(words)


def encrypt_pdf(source: BytesIO, path: Path, password: str) -> Path:
    """Writes the PDF in `source` to `path`, encrypted with `password`.

    The unencrypted document is never written to disk. Raises if
    `password` is blank, since that would silently write it in the clear.
    """
    if not password:
        raise ValueError("Expected a password. Got an empty string.")
    source.seek(0)
    writer = PdfWriter(clone_from=source)
    writer.encrypt(password, algorithm=ALGORITHM)
    with path.open("wb") as file:
        writer.write(file)
    return path
