"""Parse a Django `edc.log` into a pandas DataFrame, one row per log record.

The file is written by the `file` handler in `meta_edc.settings.logging` using the
`verbose` formatter::

    "[%(asctime)s] %(process)-5d %(thread)d %(name)-50s %(levelname)-8s %(message)s"
    datefmt="%d/%b/%Y %H:%M:%S"

Two things make this awkward for `read_csv`/`read_fwf`:

  1. The widths are *minimums*, not fixed. A logger name longer than 50 chars, or a
     pid wider than 5 digits, pushes the later columns right. So we split on runs of
     whitespace via a regex, not on offsets.
  2. `django.request` ERROR records carry `exc_info`, so each is followed by a
     multi-line traceback whose lines do not start with `[`. Those are folded into a
     `traceback` column rather than dropped or parsed as garbage rows.

Only the `django` logger writes to this file (root and `meta-trial` go to syslog), so
expect `django.request`, `django.security.*`, `django.server`, `django.db.backends`.

Run directly to parse the sample logs and report any lines the regex could not
account for::

    uv run --dev python -m meta_analytics.scripts.parse_edc_log [path ...]
"""

from __future__ import annotations

import os
import re
import sys
from collections.abc import Iterator
from functools import cache
from pathlib import Path

import pandas as pd

# ruff: noqa: T201

SAMPLES = Path(__file__).parent / "samples"

RECORD = re.compile(
    r"^\[(?P<asctime>\d{2}/[A-Za-z]{3}/\d{4} \d{2}:\d{2}:\d{2})\]\s+"
    r"(?P<process>\d+)\s+"
    r"(?P<thread>\d+)\s+"
    r"(?P<name>\S+)\s+"
    r"(?P<levelname>[A-Z]+)\s+"
    r"(?P<message>.*)$"
)

LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

COLUMNS = ["timestamp", "level", "logger", "process", "thread", "message", "traceback"]


def iter_records(path: Path) -> Iterator[dict[str, str]]:
    """Yield one dict per log record, folding continuation lines into `traceback`."""
    record: dict[str, str] | None = None
    tail: list[str] = []
    with path.open(encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if match := RECORD.match(line):
                if record is not None:
                    record["traceback"] = "\n".join(tail)
                    yield record
                record, tail = match.groupdict(), []
            elif record is not None:
                tail.append(line)
    if record is not None:
        record["traceback"] = "\n".join(tail)
        yield record


def read_edc_log(path: Path) -> pd.DataFrame:
    """Parse an edc.log written by the `verbose` formatter into a DataFrame."""
    return (
        pd.DataFrame(iter_records(path), columns=[*RECORD.groupindex, "traceback"])
        .assign(
            timestamp=lambda df: pd.to_datetime(df["asctime"], format="%d/%b/%Y %H:%M:%S"),
            process=lambda df: df["process"].astype("int64"),
            thread=lambda df: df["thread"].astype("int64"),
            logger=lambda df: df["name"].astype("category"),
            level=lambda df: pd.Categorical(df["levelname"], categories=LEVELS, ordered=True),
            message=lambda df: df["message"].str.strip(),
            traceback=lambda df: df["traceback"].replace("", pd.NA),
        )
        .loc[:, COLUMNS]
        .sort_values("timestamp", kind="stable")
        .reset_index(drop=True)
    )


def read_edc_logs(*paths: Path) -> pd.DataFrame:
    """Parse and concatenate several rotated log files, tagged by `source`.

    Deliberately does NOT de-duplicate. `asctime` is second-resolution with no
    `%(msecs)`, so two genuine records -- e.g. a bot hitting /index.php twice in the
    same second from the same worker -- are identical in every parsed field and cannot
    be told apart from a true duplicate. De-duplicating on (timestamp, process, thread,
    message) silently drops ~14% of these sample logs. If you know your inputs overlap,
    de-duplicate explicitly at the call site and accept the loss.
    """
    return (
        pd.concat([read_edc_log(p).assign(source=p.name) for p in paths])
        .sort_values("timestamp", kind="stable")
        .reset_index(drop=True)
    )


# `django.request` / `django.security.*` messages, e.g.
#   "Not Found: /favicon.ico"
#   "Internal Server Error: /subject/subject_dashboard/105-40-0338-7/"
#   "Forbidden (Referer checking failed - ... does not match any trusted origin): /i18n/"
REQUEST = re.compile(
    r"^(?P<reason>[^(:]+?)(?: \((?P<detail>.*)\))?: (?P<path>/\S*)\Z", re.DOTALL
)


def split_request_messages(df: pd.DataFrame) -> pd.DataFrame:
    """Add reason/detail/path columns extracted from request-style messages."""
    return df.join(df["message"].str.extract(REQUEST))


def exception_line(df: pd.DataFrame) -> pd.Series:
    """Last non-empty traceback line, i.e. the exception class and message."""
    return (
        df["traceback"].dropna().str.rstrip().str.rsplit("\n", n=1).str[-1].rename("exception")
    )


def unparsed_lines(path: Path) -> list[tuple[int, str]]:
    """Lines belonging to no record: text before the first `[timestamp]` header.

    Everything after a header is legitimately a continuation line, so a non-empty
    result here means the file starts mid-record (rotated log) or the formatter
    differs from the one this module assumes.
    """
    orphans: list[tuple[int, str]] = []
    with path.open(encoding="utf-8", errors="replace") as f:
        for lineno, raw in enumerate(f, start=1):
            if RECORD.match(raw):
                break
            if raw.strip():
                orphans.append((lineno, raw.rstrip("\n")))
    return orphans


def report(path: Path) -> pd.DataFrame:
    """Parse `path` and print a summary plus anything the regex could not account for."""
    total_lines = sum(1 for _ in path.open(encoding="utf-8", errors="replace"))
    df = read_edc_log(path)
    tracebacks = df["traceback"].notna()
    continuation = int(
        df.loc[tracebacks, "traceback"].str.count("\n").sum() + tracebacks.sum()
    )
    orphans = unparsed_lines(path)

    print(f"\n=== {path.name} ===")
    print(f"lines               {total_lines}")
    print(f"records             {len(df)}")
    print(f"continuation lines  {continuation}")
    print(f"unaccounted lines   {total_lines - len(df) - continuation}")
    print(f"orphans (pre-first) {len(orphans)}")
    for lineno, line in orphans[:5]:
        print(f"    {lineno}: {line[:120]}")
    print(f"span                {df['timestamp'].min()} -> {df['timestamp'].max()}")
    print(f"\nlevels\n{df['level'].value_counts().to_string()}")
    print(f"\nloggers\n{df['logger'].value_counts().head(10).to_string()}")

    parsed = split_request_messages(df)
    unmatched = parsed["path"].isna().sum()
    print(f"\nmessages not request-shaped: {unmatched} of {len(parsed)}")
    for message in parsed.loc[parsed["path"].isna(), "message"].head(5):
        print(f"    {message[:120]}")
    print(f"\ntop paths\n{parsed['path'].value_counts().head(10).to_string()}")
    exceptions = exception_line(df)
    if not exceptions.empty:
        print(f"\ntop exceptions\n{exceptions.value_counts().head(10).to_string()}")
    return df


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    paths = [Path(a) for a in args] or sorted(SAMPLES.glob("*.log"))
    if not paths:
        print("no log files given and no samples found", file=sys.stderr)
        return 1
    for path in paths:
        report(path)
    return 0


# --- reading tracebacks -------------------------------------------------------------

FRAME = re.compile(r'^\s+File "(?P<file>[^"]+)", line (?P<lineno>\d+), in (?P<func>.*)$')

CHAIN = re.compile(
    r"^(?:The above exception was the direct cause of the following exception:"
    r"|During handling of the above exception, another exception occurred:)\s*$"
)

HEADER = re.compile(r"^Traceback \(most recent call last\):\s*$")

VENDOR = re.compile(r"^.*/site-packages/|^.*/lib/python3\.\d+/")

# installed under site-packages like everything else, so match on package name
PROJECT_PREFIXES = ("edc_", "meta_")


# deployed code sits either in the venv or in a source checkout under `<root>/src/`
ROOTS = ("site-packages/", "/src/")


def _shorten(path: str) -> str:
    """Trim the install prefix: `.../site-packages/edc_metadata/x.py` -> `edc_metadata/x.py`.

    Also handles the source checkout (`/home/live/edc/src/meta_dashboard/...`), which is
    not under site-packages -- miss it and every meta_* frame is misread as vendor code.
    """
    for marker in ROOTS:
        _, sep, tail = path.partition(marker)
        if sep:
            return tail
    return path


def is_project_frame(file: str, prefixes: tuple[str, ...] = PROJECT_PREFIXES) -> bool:
    """True for frames in our own packages rather than Django/stdlib/third party."""
    return _shorten(file).startswith(prefixes)


def iter_segments(traceback: str) -> Iterator[tuple[list[dict[str, str]], str]]:
    """Split a (possibly chained) traceback into (frames, exception) pairs.

    A chained traceback contains several `Traceback (most recent call last):` blocks
    joined by "The above exception was the direct cause..." / "During handling...".
    The *last* segment holds the exception that actually surfaced.
    """
    frames: list[dict[str, str]] = []
    exception = ""
    for line in traceback.splitlines():
        if CHAIN.match(line):
            if frames or exception:
                yield frames, exception
            frames, exception = [], ""
        elif match := FRAME.match(line):
            frames.append(match.groupdict())
        elif HEADER.match(line) or not line.strip() or line[:1].isspace():
            continue  # block header, blank, or the echoed source/caret line
        else:
            exception = line.rstrip()
    if frames or exception:
        yield frames, exception


def format_traceback(traceback: str, project_only: bool = True) -> str:
    """Render a traceback as a compact, readable trace.

    With `project_only`, Django/stdlib frames are collapsed to a count so the edc_/meta_
    frames stand out; the deepest frame is always kept even if it is vendor code, since
    that is where the exception was raised.
    """
    out: list[str] = []
    segments = list(iter_segments(traceback))
    for index, (frames, exception) in enumerate(segments):
        if index:
            out.append("  caused ->")
        keep = frames
        if project_only and frames:
            keep = [f for f in frames if is_project_frame(f["file"])] or frames[-1:]
            if frames[-1] not in keep:
                keep = [*keep, frames[-1]]
        skipped = len(frames) - len(keep)
        if skipped:
            out.append(f"  ({skipped} vendor frames)")
        out.extend(f"  {_shorten(f['file'])}:{f['lineno']} {f['func']}".rstrip() for f in keep)
        out.append(f"  {exception}" if exception else "  <no exception line>")
    return "\n".join(out)


def format_record(row: pd.Series, project_only: bool = True) -> str:
    """Render one parsed log record -- header, message, then the trace."""
    head = (
        f"{row['timestamp']:%d/%b/%Y %H:%M:%S}  {row['level']}  {row['logger']}  "
        f"pid={row['process']}"
    )
    parts = [head, f"  {row['message']}"]
    if pd.notna(row.get("traceback")):
        parts.append(format_traceback(row["traceback"], project_only=project_only))
    return "\n".join(parts)


def frames_frame(df: pd.DataFrame, project_only: bool = True) -> pd.DataFrame:
    """One row per traceback frame, for asking which of our files raise most often."""
    rows: list[dict[str, object]] = []
    for index, traceback in df["traceback"].dropna().items():
        for depth, (frames, exception) in enumerate(iter_segments(traceback)):
            for frame in frames:
                if project_only and not is_project_frame(frame["file"]):
                    continue
                rows.append(
                    {
                        "record": index,
                        "segment": depth,
                        "file": _shorten(frame["file"]),
                        "lineno": int(frame["lineno"]),
                        "func": frame["func"],
                        "exception": exception,
                    }
                )
    return pd.DataFrame(
        rows, columns=["record", "segment", "file", "lineno", "func", "exception"]
    )


# --- mapping server paths onto local checkouts ---------------------------------------

# The log comes from the server, where code lives under /home/live/edc/{.venv,src}.
# Locally the same packages are one-per-repo under <SOURCE_ROOT>/<repo>/src/<package>.
SOURCE_ROOT = Path(os.environ.get("EDC_SOURCE_ROOT", Path(__file__).parents[4]))


@cache
def package_index(root: Path = SOURCE_ROOT) -> dict[str, Path]:
    """Map top-level package name -> local directory, e.g. `edc_metadata` -> Path(...)."""
    return {
        pkg.name: pkg
        for src in sorted(root.glob("*/src"))
        for pkg in sorted(src.iterdir())
        if pkg.is_dir() and (pkg / "__init__.py").exists()
    }


def localize(file: str, root: Path = SOURCE_ROOT) -> Path | None:
    """Resolve a server frame path to the local checkout, or None if not found.

    Returns None for third-party frames (django, MySQLdb) -- we only index our own
    packages, so vendor code stays unresolved by design.
    """
    relative = _shorten(file)
    package, _, tail = relative.partition("/")
    directory = package_index(root).get(package)
    if directory is None or not tail:
        return None
    candidate = directory / tail
    return candidate if candidate.exists() else None


DEF = re.compile(r"^\s*(?:async\s+)?(?:def|class)\s+(?P<name>\w+)")


def verify_frame(path: Path, lineno: int, func: str, window: int = 400) -> bool | None:
    """Does `func` still enclose `lineno` locally? None when unanswerable.

    The server runs a released version, so local line numbers drift. A False here means
    the frame's line number should not be trusted for that file.
    """
    if func in {"<module>", "<lambda>", "<listcomp>", "<genexpr>", "<dictcomp>"}:
        return None
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    if lineno > len(lines):
        return False
    for index in range(lineno - 1, max(-1, lineno - window - 1), -1):
        if match := DEF.match(lines[index]):
            return match.group("name") == func
    return False


if __name__ == "__main__":
    raise SystemExit(main())
