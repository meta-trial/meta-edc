"""
Flatten a nested tree of PDFs into a single folder.

Walks SOURCE recursively, copies every *.pdf (case-insensitive) to DEST with a
filename built from the relative folder path so no two files collide and the
provenance is preserved. Skips .DS_Store and other hidden junk.

Also writes a manifest CSV (manifest.csv) mapping source -> destination so the
result is auditable.

Naming scheme:
    lab_results/Amana/105-20-0033-6/1060/AHM FBC.pdf
    -> Amana__105-20-0033-6__1060__AHM FBC.pdf

Edit SOURCE / DEST at the top if you want different locations.
"""

from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

# ---- configure ------------------------------------------------------------

SOURCE = Path.home() / "Downloads" / "lab_results"
DEST = Path.home() / "Downloads" / "lab_results_flat" / "lab_results_flat"
SEP = "__"  # joins path components in the flattened filename

# ---------------------------------------------------------------------------


def flatten_name(pdf: Path, source_root: Path) -> str:
    """Build a single flat filename from the file's path relative to source_root."""
    rel = pdf.relative_to(source_root)
    parts = list(rel.parts)
    # parts == [site, subject_id, visit, ..., filename.pdf]
    # If the file sits directly under source_root, just use its name.
    if len(parts) == 1:
        return parts[0]
    folder_parts = parts[:-1]
    filename = parts[-1]
    # Normalize whitespace inside individual components but keep them readable.
    folder_parts = [p.strip() for p in folder_parts]
    return SEP.join([*folder_parts, filename])


def main() -> int:
    if not SOURCE.exists():
        print(f"ERROR: source not found: {SOURCE}", file=sys.stderr)  # noqa T201
        return 1

    DEST.mkdir(parents=True, exist_ok=True)

    pdfs = [p for p in SOURCE.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf"]
    print(f"Found {len(pdfs)} PDF(s) under {SOURCE}")  # noqa T201

    manifest_rows: list[tuple[str, str, int]] = []
    collisions = 0
    copied = 0

    for src in pdfs:
        target_name = flatten_name(src, SOURCE)
        target = DEST / target_name

        # Defensive collision handling. With path-prefixed names this should be
        # very rare, but if two paths somehow produce the same name (e.g. a
        # folder/file naming quirk), append a numeric suffix.
        if target.exists():
            collisions += 1
            stem = target.stem
            suffix = target.suffix
            i = 2
            while (DEST / f"{stem} ({i}){suffix}").exists():
                i += 1
            target = DEST / f"{stem} ({i}){suffix}"

        shutil.copy2(src, target)
        copied += 1
        manifest_rows.append((str(src), target.name, src.stat().st_size))

    manifest_path = DEST / "manifest.csv"
    with manifest_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["source_path", "flat_filename", "size_bytes"])
        writer.writerows(manifest_rows)

    print(f"Copied {copied} PDFs to {DEST}")  # noqa T201
    if collisions:
        print(f"Resolved {collisions} filename collision(s) with numeric suffixes")  # noqa T201
    print(f"Manifest: {manifest_path}")  # noqa T201
    return 0


if __name__ == "__main__":
    sys.exit(main())
