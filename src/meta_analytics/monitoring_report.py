# ruff: noqa: PD008, PD010, PD015, PLR0912, PLR0913, PLR0915, C901, ARG001, F841, RET504
"""Generate the META3 monitoring report (PDF).

Ported from ``meta_analytics/notebooks/monitoring_report.ipynb``.

The public entry point is :func:`generate_monitoring_report`, which runs
the full pipeline of ~15 tables and writes a PDF to the given path.

The management command ``generate_monitoring_report`` is a thin wrapper
around this function.

WeasyPrint system library requirements
--------------------------------------
WeasyPrint (>=53) is a pure-Python renderer but links to system libraries
via ctypes. Install them before running the report:

Ubuntu / Debian (24.04 verified)::

    sudo apt install -y libpango-1.0-0 libpangoft2-1.0-0

macOS (Homebrew)::

    brew install pango

On Apple Silicon, if WeasyPrint cannot find the libs, export::

    export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH

Cairo and GDK-Pixbuf are *not* required by WeasyPrint 53+.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from clinicedc_constants import YES
from django_pandas.io import read_frame
from edc_appointment.analytics import get_appointment_df
from edc_appointment.constants import (
    CANCELLED_APPT,
    MISSED_APPT,
    NEW_APPT,
    ONTIME_APPT,
    SCHEDULED_APPT,
    UNSCHEDULED_APPT,
)
from edc_pdutils.dataframes import get_subject_visit
from edc_visit_schedule.models import SubjectScheduleHistory
from great_tables import html, loc, md, style
from scipy.stats import chi2
from weasyprint import HTML

from meta_analytics.dataframes import (
    GlucoseEndpointsByDate2,
    get_eos_df,
    get_glucose_df,
    get_screening_df,
)
from meta_analytics.utils import df_as_great_table, df_as_great_table2
from meta_consent.models import SubjectConsentV1Ext
from meta_visit_schedule.constants import (
    MONTH15,
    MONTH18,
    MONTH21,
    MONTH27,
    MONTH30,
    MONTH33,
    MONTH39,
)

__all__ = ["generate_monitoring_report"]

_ = (YES, SCHEDULED_APPT, UNSCHEDULED_APPT)  # used by pandas .query(@CONST) strings

STUDY_TITLE_DEFAULT = "META3 - Metformin treatment for diabetes prevention in Africa"

LATE_EXCLUSION_REASON = (
    "Patient fulfilled late exclusion criteria "
    "(due to abnormal blood values or raised blood pressure at enrolment"
)

COLUMN_HEADERS = {
    "label": "Label",
    "visit_code": "Visit code",
    "10": "Hindu Mandal",
    "20": "Amana",
    "30": "Temeke",
    "40": "Mwananyamala",
    "60": "Mnazi Moja",
    "total": "Total",
}
COLUMN_HEADERS_WITH_STR = {
    "label": "Label",
    "10_str": "Hindu Mandal",
    "20_str": "Amana",
    "30_str": "Temeke",
    "40_str": "Mwananyamala",
    "60_str": "Mnazi Moja",
    "total_str": "Total",
}


# ---------------------------------------------------------------------------
# helpers (extracted from the notebook's inline defs)
# ---------------------------------------------------------------------------
def _get_row_df(row_df: pd.DataFrame, label: str | None = None, **kwargs) -> pd.DataFrame:
    row_df = row_df.groupby(by=["site_id"]).site_id.count().to_frame(name="n")
    row_df["label"] = label
    row_df = row_df.reset_index()
    row_df = row_df.pivot(index="label", values="n", columns="site_id").reset_index()
    row_df.columns.name = ""
    for site in [10, 20, 30, 40, 60]:
        if site not in row_df.columns:
            row_df[site] = None
    return row_df.reset_index(drop=True)


def _get_row_by_df(
    row_df: pd.DataFrame, label: str, category_labels: list[str]
) -> pd.DataFrame:
    row_df = row_df.groupby(by=["site_id"]).site_id.count().to_frame(name="n")
    row_df["label"] = label
    row_df = row_df.reset_index()
    row_df = row_df.pivot(index="label", values="n", columns="site_id").reset_index()
    row_df.columns.name = ""
    for cat_label in category_labels:
        if cat_label not in row_df.columns:
            row_df[cat_label] = None
    return row_df.reset_index(drop=True)


def _get_table_df(
    df_source: pd.DataFrame,
    visit_code: float | None = None,
    month_label: str | None = None,
    visit_codes: list[float] | None = None,
    get_row_func: Callable | None = None,
    category_labels: list[str] | None = None,
) -> pd.DataFrame:
    get_row_df_func = get_row_func or _get_row_df
    if visit_code:
        df_month = df_source[df_source.visit_code == visit_code].copy()
    elif visit_codes:
        df_month = df_source[df_source.visit_code.isin(visit_codes)].copy()
    elif month_label:
        df_month = df_source.copy()
    else:
        df_month = df_source.copy()

    row_df = df_month.copy()
    table_df = get_row_df_func(row_df, "Total (n)", category_labels=category_labels)

    specs = [
        ("OGTT <7.8; FBG <6.1", (df_month.ogtt_value < 7.8) & (df_month.fbg_value < 6.1)),
        (
            "OGTT <7.8; FBG >=6.1 <7.0",
            (df_month.ogtt_value < 7.8)
            & (df_month.fbg_value >= 6.1)
            & (df_month.fbg_value < 7.0),
        ),
        ("OGTT <7.8; FBG >=7.0", (df_month.ogtt_value < 7.8) & (df_month.fbg_value >= 7.0)),
        (
            "OGTT ≥7.8 to <11.1; FBG <6.1",
            (df_month.ogtt_value >= 7.8)
            & (df_month.ogtt_value < 11.1)
            & (df_month.fbg_value < 6.1),
        ),
        (
            "OGTT ≥7.8 to <11.1; FBG >=6.1 <7.0",
            (df_month.ogtt_value >= 7.8)
            & (df_month.ogtt_value < 11.1)
            & (df_month.fbg_value >= 6.1)
            & (df_month.fbg_value < 7.0),
        ),
        (
            "OGTT ≥7.8 to <11.1; FBG >=7.0",
            (df_month.ogtt_value >= 7.8)
            & (df_month.ogtt_value < 11.1)
            & (df_month.fbg_value >= 7.0),
        ),
        ("OGTT ≥11.1; FBG <6.1", (df_month.ogtt_value >= 11.1) & (df_month.fbg_value < 6.1)),
        (
            "OGTT ≥11.1; FBG >=6.1 <7.0",
            (df_month.ogtt_value >= 11.1)
            & (df_month.fbg_value >= 6.1)
            & (df_month.fbg_value < 7.0),
        ),
        (
            "OGTT ≥11.1; FBG >=7.0",
            (df_month.ogtt_value >= 11.1) & (df_month.fbg_value >= 7.0),
        ),
        ("Missing OGTT", df_month.ogtt_value.isna()),
    ]
    for label, mask in specs:
        table_df = pd.concat(
            [
                table_df,
                get_row_df_func(df_month[mask].copy(), label, category_labels=category_labels),
            ]
        )
    return table_df


def _format_table_df(tbl_df: pd.DataFrame, add_totals: bool | None = None) -> pd.DataFrame:
    add_totals = True if add_totals is None else add_totals
    tbl_df = tbl_df.fillna(0.0)
    tbl_df["total"] = tbl_df.iloc[:, 1:].sum(axis=1)
    tbl_df = tbl_df.reset_index(drop=True)

    if add_totals:
        df_last = tbl_df[1:].sum().to_frame()
        df_last.loc["label"] = np.nan
        df_last = df_last.reset_index()
        df_last.columns = ["label", "value"]
        df_last = df_last.pivot_table(columns="label", values="value").reset_index(drop=True)
        df_last.columns.name = ""
        df_last["label"] = "Totals"
        tbl_df = pd.concat([tbl_df, df_last]).reset_index(drop=True)

    tbl_df.columns = ["label", "10", "20", "30", "40", "60", "total"]

    for site in ["10", "20", "30", "40", "60", "total"]:
        tbl_df[f"{site}_perc"] = (
            (tbl_df[site] / tbl_df.iloc[0][site]) * 100 if tbl_df.iloc[0][site] > 0 else 0
        )
        tbl_df[f"{site}_perc_str"] = tbl_df[f"{site}_perc"].map("{:.1f}".format)

    for site in ["10", "20", "30", "40", "60", "total"]:
        tbl_df[f"{site}_str"] = tbl_df[[f"{site}", f"{site}_perc_str"]].apply(
            lambda x: " (".join(x.astype(str)), axis=1
        )
        tbl_df[f"{site}_str"] = tbl_df[f"{site}_str"] + ")"

    cols = ["label", *[f"{site}_str" for site in ["10", "20", "30", "40", "60", "total"]]]
    return tbl_df[cols]


def _get_fbg_value(r):
    if not pd.isna(r.get("converted_fbg2_value")):
        return r["converted_fbg2_value"]
    return r["converted_fbg_value"]


def _get_ogtt_value(r):
    if not pd.isna(r.get("converted_ogtt2_value")):
        return r["converted_ogtt2_value"]
    return r["converted_ogtt_value"]


def _get_table7_df(df_source: pd.DataFrame, visit_code: float) -> pd.DataFrame:
    df_month = df_source[
        (df_source.visit_code >= visit_code) & (df_source.visit_code <= visit_code + 0.9)
    ].copy()
    row_df = df_month.copy()
    table_df = _get_row_df(row_df, "Total (n)")
    table_df = pd.concat(
        [table_df, _get_row_df(df_month[df_month.fbg_value < 6.1].copy(), "FBG <6.1")]
    )
    table_df = pd.concat(
        [
            table_df,
            _get_row_df(
                df_month[(df_month.fbg_value >= 6.1) & (df_month.fbg_value < 7.0)].copy(),
                "FBG >=6.1 <7.0",
            ),
        ]
    )
    table_df = pd.concat(
        [table_df, _get_row_df(df_month[df_month.fbg_value >= 7.0].copy(), "FBG >=7.0")]
    )
    return table_df


def _get_schedule_df(
    df_subjecthistory: pd.DataFrame,
    onschedule_model: str,
    offschedule_model: str,
    mode: str,
) -> pd.DataFrame:
    columns = {k: f"{k}_{mode}" for k in ["10", "20", "30", "40", "60"]}
    df_schedule = (
        df_subjecthistory.query(
            f"onschedule_model==@onschedule_model and "
            f"offschedule_model==@offschedule_model and "
            f"offschedule_datetime.{'isna' if mode == 'on' else 'notna'}()"
        )
        .groupby(by=["onschedule_model", "site_id"])
        .size()
        .reset_index()
        .pivot_table(index="onschedule_model", columns="site_id", values=0, observed=True)
        .reset_index()
        .rename(columns={"onschedule_model": "schedule", **columns})
        .fillna(0)
        .copy()
    )
    df_schedule.columns.name = ""
    return df_schedule


def _get_df_main(
    df_visit: pd.DataFrame,
    df_endpoint: pd.DataFrame,
    lower_days: float | None = None,
    upper_days: float | None = None,
):
    if not lower_days:
        lower_days = -1
    df_eos = get_eos_df()
    df_eos_excluded = (
        df_eos.query(
            "followup_days>@lower_days and followup_days<=@upper_days and "
            "offstudy_reason.isin([@LATE_EXCLUSION_REASON])"
        )
        .copy()
        .reset_index()
    )
    df_visit_final = (
        df_visit.query(
            "@lower_days<followup_days<=@upper_days and reason!='missed' and visit_code<2000.0"
        )
        .merge(
            df_eos_excluded[["subject_identifier"]],
            on="subject_identifier",
            how="left",
            suffixes=("", "_y"),
            indicator=True,
        )
        .query("_merge=='left_only'")
        .drop(columns=["_merge"])
    )
    df_main = (
        df_visit_final.groupby(by=["subject_identifier"])[
            ["baseline_datetime", "visit_datetime", "followup_days"]
        ]
        .max()
        .reset_index()
    )
    df_main = df_main.merge(
        df_endpoint.query("days_to_event>@lower_days")[
            ["subject_identifier", "endpoint_label", "endpoint_type", "days_to_event"]
        ],
        how="left",
        on=["subject_identifier"],
    ).reset_index(drop=True)
    if lower_days >= 365.25:
        df_main["followup_days"] = df_main["followup_days"] - lower_days
    df_main["followup_years"] = df_main["followup_days"] / 365.25
    return (
        df_main,
        len(df_main),
        len(
            df_main.query("@lower_days<days_to_event<=@upper_days and endpoint_label.notna()")
        ),
    )


def _get_rate_and_ci(events: int, person_years_total: float):
    lower_ci = (chi2.ppf(0.025, 2 * events) / (2 * person_years_total)) * 1000
    upper_ci = (chi2.ppf(0.975, 2 * (events + 1)) / (2 * person_years_total)) * 1000
    return events / person_years_total * 1000, lower_ci, upper_ci


def _get_incidence_data(
    df_visit: pd.DataFrame,
    df_endpoint: pd.DataFrame,
    term: str,
    lower_days: float,
    upper_days: float,
):
    df_main, subjects, events = _get_df_main(
        df_visit, df_endpoint, lower_days=lower_days, upper_days=upper_days
    )
    person_years_total = df_main.followup_years.sum()
    return {
        term: [
            person_years_total,
            subjects,
            events,
            *_get_rate_and_ci(events, person_years_total),
        ]
    }


# ---------------------------------------------------------------------------
# main entry point
# ---------------------------------------------------------------------------
def generate_monitoring_report(
    output_path: Path | str,
    *,
    cutoff_date: datetime | None = None,
    data_download_date: datetime | None = None,
    end_of_trial_date: datetime | None = None,
    study_title: str = STUDY_TITLE_DEFAULT,
    verbose: bool = False,
) -> Path:
    """Build the monitoring report and write to ``output_path`` as a PDF.

    All dates default to sensible values if omitted:
      - ``cutoff_date``: end of *today* (UTC)
      - ``data_download_date``: start of *today* (UTC)
      - ``end_of_trial_date``: ``cutoff_date`` + ~60 days
    """
    now_utc = datetime.now(tz=ZoneInfo("UTC"))
    if data_download_date is None:
        data_download_date = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    if cutoff_date is None:
        cutoff_date = now_utc.replace(hour=23, minute=59, second=0, microsecond=0)
    if end_of_trial_date is None:
        end_of_trial_date = cutoff_date.replace(hour=0, minute=0, second=0, microsecond=0)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_data: list[str] = []
    document_title = (
        f"<h2>Monitoring Report: {cutoff_date.strftime('%B %Y')}</h2>"
        f"<h5>Data Download: {data_download_date.strftime('%d %B %Y')} "
        f"using cutoff date of {cutoff_date.strftime('%d %B %Y')}</h5>"
    )

    # --- base dataframes -----------------------------------------------------
    df_visit = get_subject_visit("meta_subject.subjectvisit")
    df_visit_1691 = df_visit.copy()

    df_eos = get_eos_df()
    df_eos_excluded = (
        df_eos.query("offstudy_reason.isin([@LATE_EXCLUSION_REASON])").copy().reset_index()
    )
    df_visit = (
        df_visit.merge(
            df_eos_excluded[["subject_identifier", "offstudy_datetime", "offstudy_reason"]],
            on="subject_identifier",
            how="left",
            indicator=True,
        )
        .query("_merge=='left_only'")
        .drop(columns=["_merge"])
    )
    df_visit = df_visit[df_visit.appt_datetime <= cutoff_date]

    df_appointments = get_appointment_df()
    df_appointments["site_id"] = df_appointments.site_id.astype(str)
    df_appointments = (
        df_appointments.merge(
            df_eos_excluded[["subject_identifier", "offstudy_datetime", "offstudy_reason"]],
            on="subject_identifier",
            how="left",
            indicator=True,
        )
        .query("_merge=='left_only'")
        .drop(columns=["_merge"])
    )

    cls = GlucoseEndpointsByDate2(verbose=verbose)
    df_endpoint = cls.endpoint_df.copy()
    df_glucose = get_glucose_df()

    enrolled_1691 = df_visit_1691.copy()
    enrolled_1691["site_id"] = enrolled_1691["site_id"].astype(str)
    enrolled_1691_pivot = (
        enrolled_1691.query("visit_code==1000.0")
        .groupby(["site_id"])
        .size()
        .reset_index()
        .pivot_table(columns="site_id", values=0, observed=True)
    )
    enrolled_1691_pivot.columns.name = ""
    enrolled_1691_pivot["total"] = enrolled_1691_pivot[["10", "20", "30", "40", "60"]].sum(
        axis=1
    )

    # --- Table 1a: Visits completed to date ---------------------------------
    df_tbl1 = (
        df_visit[
            (df_visit.visit_code_sequence == 0)
            & (df_visit.appt_timing == ONTIME_APPT)
            & ~(df_visit.appt_status.isin([NEW_APPT, CANCELLED_APPT]))
        ]
        .groupby(by=["visit_code", "site_id"])
        .size()
        .to_frame()
        .reset_index()
    )
    df_tbl1.columns = ["visit_code", "site_id", "visits"]
    df1 = df_tbl1.pivot(index="visit_code", columns="site_id", values="visits").reset_index()
    df1.columns.name = None
    df1.columns = ["visit_code", "10", "20", "30", "40", "60"]
    df1["total"] = df1[["10", "20", "30", "40", "60"]].sum(axis=1)
    df_attended = df1.fillna(0).reset_index(drop=True).fillna(0.0)

    gt = df_as_great_table(
        df_attended[["visit_code", "10", "20", "30", "40", "60", "total"]],
        title="Table 1a: Visits completed to date",
    )
    gt = (
        gt.cols_label({k: v for k, v in COLUMN_HEADERS.items() if k != "label"})
        .cols_align(align="center", columns=["10", "20", "30", "40", "60", "total"])
        .cols_align(align="left", columns=["visit_code"])
        .data_color(
            columns=["visit_code"],
            palette=["lavender", "thistle"],
            domain=[2000, 5000],
            na_color="white",
        )
        .tab_source_note(
            source_note=(
                "Excludes visit reports submitted for participants "
                "eventually withdrawn on late exclusion criteria."
            )
        )
    )
    html_data.append(gt.as_raw_html())

    # --- Table 1b: Total scheduled appointments -----------------------------
    df_appt_pivot = (
        df_appointments.query("appt_reason==@SCHEDULED_APPT")
        .merge(
            df_eos_excluded[["subject_identifier"]],
            on="subject_identifier",
            how="left",
            indicator=True,
        )
        .query("_merge=='left_only'")
        .drop(columns=["_merge"])
        .reset_index(drop=True)
        .groupby(["visit_code", "site_id"])
        .size()
        .to_frame()
        .reset_index()
        .pivot(index="visit_code", columns="site_id", values=0)
        .reset_index()
        .fillna(0)
    )
    df_appt_pivot["total"] = df_appt_pivot.iloc[:, 1:].sum(axis=1)
    df_appt_pivot.columns.name = None
    gt = df_as_great_table(
        df_appt_pivot,
        title="Table 1b: Total appointments",
        subtitle="Total possible appointments not including unscheduled appointments",
    )
    gt = (
        gt.cols_label({k: v for k, v in COLUMN_HEADERS.items() if k != "label"})
        .cols_align(align="center", columns=["10", "20", "30", "40", "60", "total"])
        .cols_align(align="left", columns=["visit_code"])
        .data_color(
            columns=["visit_code"],
            palette=["lavender", "thistle"],
            domain=[2000, 5000],
            na_color="white",
        )
    )
    html_data.append(gt.as_raw_html())

    # --- Table 1c: Past appointments not attended/not reported ---------------
    df_appt_pivot = (
        df_appointments.query(
            "appt_datetime<@cutoff_date and appt_reason==@SCHEDULED_APPT and "
            "appt_timing==@ONTIME_APPT and appt_status.isin([@NEW_APPT])"
        )
        .merge(
            df_eos_excluded[["subject_identifier"]],
            on="subject_identifier",
            how="left",
            indicator=True,
        )
        .query("_merge=='left_only'")
        .drop(columns=["_merge"])
        .reset_index(drop=True)
        .groupby(["visit_code", "site_id"])
        .size()
        .to_frame()
        .reset_index()
        .pivot(index="visit_code", columns="site_id", values=0)
        .reset_index()
        .fillna(0)
    )
    df_appt_pivot["total"] = df_appt_pivot.iloc[:, 1:].sum(axis=1)
    df_appt_pivot.columns.name = None
    gt = df_as_great_table(
        df_appt_pivot,
        title="Table 1c: Past appointments not attended/not reported",
        subtitle="Expected by now but no information provided by site",
    )
    gt = (
        gt.cols_label({k: v for k, v in COLUMN_HEADERS.items() if k != "label"})
        .cols_align(align="center", columns=["10", "20", "30", "40", "60", "total"])
        .cols_align(align="left", columns=["visit_code"])
        .data_color(
            columns=["visit_code"],
            palette=["lavender", "thistle"],
            domain=[2000, 5000],
            na_color="white",
        )
        .tab_source_note(
            source_note=(
                f"Scheduled appointment date is before {cutoff_date.strftime('%d %B %Y')}."
            )
        )
    )
    html_data.append(gt.as_raw_html())

    # --- Table 1d: Unscheduled appointments ----------------------------------
    df_appt = (
        df_appointments.query(
            "appt_reason==@UNSCHEDULED_APPT and appt_timing==@ONTIME_APPT and "
            "appt_status!=@NEW_APPT"
        )
        .merge(
            df_eos_excluded[["subject_identifier"]],
            on="subject_identifier",
            how="left",
            indicator=True,
        )
        .query("_merge=='left_only'")
        .drop(columns=["_merge"])
        .reset_index(drop=True)
        .copy()
        .reset_index(drop=True)
    )
    df_appt["visit_code"] = df_appt["visit_code"].astype(int).astype(str)
    subjects_with_unscheduled = df_appt.subject_identifier.nunique()

    df_appt_pivot = (
        df_appt.groupby(["visit_code", "site_id"])
        .size()
        .to_frame()
        .reset_index()
        .pivot(index="visit_code", columns="site_id", values=0)
        .reset_index()
        .fillna(0)
    )
    df_appt_pivot["total"] = df_appt_pivot.iloc[:, 1:].sum(axis=1)
    df_appt_pivot.columns.name = None
    df_appt_pivot[["10", "20", "30", "40", "60", "total"]] = df_appt_pivot[
        ["10", "20", "30", "40", "60", "total"]
    ].astype("float64")
    sum_row = df_appt_pivot.select_dtypes(include="float64").sum()
    sum_row["visit_code"] = "Total"
    df_appt_pivot = pd.concat([df_appt_pivot, pd.DataFrame(sum_row).T], axis=0).reset_index(
        drop=True
    )

    gt = df_as_great_table(
        df_appt_pivot,
        title="Table 1d: Unscheduled appointments",
        subtitle="Appointments with sequence>0 grouped by visit code",
    )
    gt = (
        gt.cols_label({k: v for k, v in COLUMN_HEADERS.items() if k != "label"})
        .cols_align(align="center", columns=["10", "20", "30", "40", "60", "total"])
        .cols_align(align="left", columns=["visit_code"])
        .data_color(
            columns=["visit_code"],
            palette=["lavender", "thistle"],
            domain=[2000, 5000],
            na_color="white",
        )
        .fmt_number(columns=["10", "20", "30", "40", "60", "total"], decimals=0)
        .tab_source_note(
            source_note=(
                f"{subjects_with_unscheduled} participants had at least one "
                "unscheduled appointment."
            )
        )
    )
    html_data.append(gt.as_raw_html())

    # --- Table 1e: Future scheduled appointments -----------------------------
    df_appt_pivot = (
        df_appointments.query(
            "@cutoff_date<=appt_datetime<@end_of_trial_date and "
            "appt_reason==@SCHEDULED_APPT and appt_timing==@ONTIME_APPT and "
            "appt_status.isin([@NEW_APPT])"
        )
        .merge(
            df_eos_excluded[["subject_identifier"]],
            on="subject_identifier",
            how="left",
            indicator=True,
        )
        .query("_merge=='left_only'")
        .drop(columns=["_merge"])
        .reset_index(drop=True)
        .groupby(["visit_code", "site_id"])
        .size()
        .to_frame()
        .reset_index()
        .pivot(index="visit_code", columns="site_id", values=0)
        .reset_index()
        .fillna(0)
    )
    df_appt_pivot["total"] = df_appt_pivot.iloc[:, 1:].sum(axis=1)
    df_appt_pivot.columns.name = None
    gt = df_as_great_table(df_appt_pivot, title="Table 1e: Future appointments")
    gt = (
        gt.cols_label({k: v for k, v in COLUMN_HEADERS.items() if k != "label"})
        .cols_align(align="center", columns=["10", "20", "30", "40", "60", "total"])
        .cols_align(align="left", columns=["visit_code"])
        .data_color(
            columns=["visit_code"],
            palette=["lavender", "thistle"],
            domain=[2000, 5000],
            na_color="white",
        )
        .fmt_number(columns=["10", "20", "30", "40", "60", "total"], decimals=0)
        .tab_source_note(
            source_note=(
                f"Scheduled appointment date is on or after "
                f"{cutoff_date.strftime('%d %B %Y')} and before "
                f"{end_of_trial_date.strftime('%d %B %Y')}."
            )
        )
    )
    html_data.append(gt.as_raw_html())

    # --- Table 2a: Visits Missed to Date -------------------------------------
    subject_count_missed = (
        df_visit.query(
            "visit_code_sequence==0 and appt_timing==@MISSED_APPT and "
            "~appt_status.isin([@NEW_APPT, @CANCELLED_APPT])"
        )
    ).subject_identifier.nunique()

    df_tbl = (
        df_visit[
            (df_visit.visit_code_sequence == 0)
            & (df_visit.appt_timing == MISSED_APPT)
            & ~(df_visit.appt_status.isin([NEW_APPT, CANCELLED_APPT]))
        ]
        .groupby(by=["visit_code", "site_id"])
        .size()
        .to_frame()
        .reset_index()
    )
    df_tbl.columns = ["visit_code", "site_id", "visits"]
    df_tbl_pivot = df_tbl.pivot(
        index="visit_code", columns="site_id", values="visits"
    ).reset_index()
    df_tbl_pivot.columns.name = None
    df_tbl_pivot.columns = ["visit_code", "10", "20", "30", "40", "60"]
    df_tbl_pivot["total"] = df_tbl_pivot[["10", "20", "30", "40", "60"]].sum(axis=1)
    df_missed = df_tbl_pivot.fillna(0).copy().set_index(["visit_code"])

    df_attended_display = df_attended.copy().set_index(["visit_code"])
    attended_and_missed = df_attended_display + df_missed
    attended_and_missed = attended_and_missed.fillna(0).reset_index().set_index(["visit_code"])
    attended_and_missed_perc = df_missed / attended_and_missed
    attended_and_missed_perc = (
        attended_and_missed_perc.fillna(0).reset_index().set_index(["visit_code"])
    )

    df_result = df_missed.merge(
        attended_and_missed_perc, on=["visit_code"], suffixes=("", "_perc")
    )
    for col in ["10", "20", "30", "40", "60", "total"]:
        col_perc = f"{col}_perc"
        df_result[col] = df_result.apply(
            lambda x, c=col, cp=col_perc: f"{x[c]} ({x[cp] * 100:.2f})", axis=1
        )
    df_result = (
        df_result.reset_index().sort_values(by=["visit_code"], ascending=True).fillna(0.0)
    )

    df_table = df_result[["visit_code", "10", "20", "30", "40", "60", "total"]].copy()
    gt = df_as_great_table(
        df_table,
        title="Table 2a: Visits Missed to Date",
        subtitle="as % of Visits Attended + Visits Missed",
    )
    gt = (
        gt.cols_label({k: v for k, v in COLUMN_HEADERS.items() if k != "label"})
        .cols_align(align="center", columns=["10", "20", "30", "40", "60", "total"])
        .cols_align(align="left", columns=["visit_code", "label"])
        .tab_style(
            style=[style.fill(color="snow"), style.text(color="black")],
            locations=loc.body(columns=[0], rows=list(range(0, len(df_table)))),
        )
        .tab_source_note(
            source_note=f"{subject_count_missed} participants had at least one missed visit."
        )
    )
    html_data.append(gt.as_raw_html())

    # --- Table 2b: Number of missed visits by participant --------------------
    df_tbl = (
        df_visit[
            (df_visit.visit_code_sequence == 0)
            & (df_visit.appt_timing == MISSED_APPT)
            & ~(df_visit.appt_status.isin([NEW_APPT, CANCELLED_APPT]))
        ]
        .groupby(by=["subject_identifier", "site_id"])
        .size()
        .to_frame()
        .reset_index()
    )
    df_tbl.columns = ["subject_identifier", "site_id", "missed_count"]
    df_tbl["category"] = pd.cut(
        df_tbl["missed_count"],
        bins=[0, 1, 3, 5, 7, 100],
        labels=["Missed at least 1", "2 to 3", "4 to 5", "6 to 7", "missed more than 7"],
    )
    df_tbl_pivot = df_tbl.pivot_table(
        index="category",
        columns="site_id",
        values="missed_count",
        observed=False,
        aggfunc="count",
    ).reset_index()
    df_tbl_pivot["total"] = df_tbl_pivot.select_dtypes(include="int").sum(axis=1, skipna=True)
    sum_row = df_tbl_pivot.select_dtypes(include="int64").sum()
    sum_row["category"] = "Total"
    df_tbl_pivot = pd.concat([df_tbl_pivot, sum_row.to_frame().T], axis=0).rename(
        columns={10: "10", 20: "20", 30: "30", 40: "40", 60: "60"}
    )
    gt = df_as_great_table(
        df_tbl_pivot, title="Table 2b: Number of participants who missed one or more visits"
    )
    gt = (
        gt.cols_label(
            {
                "category": "Category",
                **{
                    k: v for k, v in COLUMN_HEADERS.items() if k not in ["visit_code", "label"]
                },
            }
        )
        .cols_align(align="center", columns=["10", "20", "30", "40", "60", "total"])
        .cols_align(align="left", columns=["category"])
    )
    html_data.append(gt.as_raw_html())

    # --- Table 3: OGTT and FBG at Enrolment ---------------------------------
    subjects = df_visit.subject_identifier.unique()
    df_screening = get_screening_df().query(
        "consented==True and subject_identifier.isin(@subjects)"
    )
    df_screening["visit_code"] = "Enrol"
    df_screening["fbg_value"] = df_screening.apply(_get_fbg_value, axis=1)
    df_screening["ogtt_value"] = df_screening.apply(_get_ogtt_value, axis=1)
    df_screening["site_id"] = df_screening.site.astype(int)
    df_screening = df_screening.drop(columns=["site"])
    df_table3 = _format_table_df(_get_table_df(df_screening, month_label="enrol")).fillna(0.0)

    gt = df_as_great_table(df_table3, title="Table 3a: OGTT and FBG at Screening / Enrolment")
    column_headers_enrol = {
        k: v for k, v in COLUMN_HEADERS_WITH_STR.items() if k != "visit_code"
    }
    gt = (
        gt.cols_label(column_headers_enrol)
        .cols_align(
            align="center",
            columns=["10_str", "20_str", "30_str", "40_str", "60_str", "total_str"],
        )
        .cols_align(align="left", columns=["label"])
        .cols_width(cases={"label": "35%"})
        .tab_source_note(
            source_note=(
                "Excluding patients eventually withdrawn for `late exclusion` criteria"
            )
        )
    )
    html_data.append(gt.as_raw_html())

    # --- Table 4: 12-month ---------------------------------------------------
    def _ogtt_fbg_visit_table(
        title: str,
        visit_code: float | None = None,
        visit_codes: list[float] | None = None,
    ):
        df_t = _format_table_df(
            _get_table_df(df_glucose, visit_code=visit_code, visit_codes=visit_codes)
        ).fillna(0.0)
        gt_local = df_as_great_table(df_t, title=title)
        note = None
        if visit_code is not None:
            missing_ogtt = sorted(
                df_glucose.query(
                    "visit_code==@visit_code and ogtt_value.isna()"
                ).subject_identifier.to_list()
            )
            if missing_ogtt:
                note = html("<BR>".join(missing_ogtt))
        gt_local = (
            gt_local.cols_label(COLUMN_HEADERS_WITH_STR)
            .cols_align(
                align="center",
                columns=["10_str", "20_str", "30_str", "40_str", "60_str", "total_str"],
            )
            .cols_align(align="left", columns=["label"])
            .cols_width(cases={"label": "35%"})
        )
        if note is not None:
            gt_local = gt_local.tab_source_note(source_note=note)
        return gt_local

    html_data.append(
        _ogtt_fbg_visit_table(
            "Table 4: OGTT and FBG at 12-month visit", visit_codes=[1120.0]
        ).as_raw_html()
    )
    html_data.append(
        _ogtt_fbg_visit_table(
            "Table 5: OGTT and FBG at 24-month visit", visit_code=1240.0
        ).as_raw_html()
    )
    html_data.append(
        _ogtt_fbg_visit_table(
            "Table 6: OGTT and FBG at 36-month visit", visit_code=1360.0
        ).as_raw_html()
    )

    # --- Table 7: Any OGTT>=11.1 ever ---------------------------------------
    row_df = df_glucose[df_glucose.ogtt_value >= 11.1].copy()
    table_df_7 = _format_table_df(_get_row_df(row_df, "Total (n)"))
    df_table_7 = table_df_7[:1].fillna(0.0).copy().reset_index(drop=True)
    gt = df_as_great_table(df_table_7, title="Table 7: Any OGTT>11.1 ever")
    gt = (
        gt.cols_label(COLUMN_HEADERS_WITH_STR)
        .cols_align(
            align="center",
            columns=["10_str", "20_str", "30_str", "40_str", "60_str", "total_str"],
        )
        .cols_align(align="left", columns=["label"])
        .cols_width(cases={"label": "35%"})
    )
    html_data.append(gt.as_raw_html())

    # --- Table 8: Interim FBG ------------------------------------------------
    frames = []
    for visit_start, month_label in [
        (1150.0, MONTH15),
        (1180.0, MONTH18),
        (1210.0, MONTH21),
        (1270.0, MONTH27),
        (1300.0, MONTH30),
        (1330.0, MONTH33),
        (1390.0, MONTH39),
    ]:
        df_t = _format_table_df(_get_table7_df(df_glucose, visit_start), add_totals=False)
        df_t["visit_code"] = month_label
        frames.append(df_t)
    df_table_8 = pd.concat(frames).reset_index(drop=True).fillna(0.0)
    column_headers_with_vc = {"visit_code": "Visit Code", **COLUMN_HEADERS_WITH_STR}
    gt = df_as_great_table2(df_table_8, title="Table 8: Interim FBG results")
    gt = (
        gt.cols_label(column_headers_with_vc)
        .cols_move_to_start(columns="visit_code")
        .cols_align(
            align="center",
            columns=["10_str", "20_str", "30_str", "40_str", "60_str", "total_str"],
        )
        .cols_align(align="left", columns=["visit_code", "label"])
        .cols_width(cases={"label": "15%"})
        .tab_style(
            style=[style.text(color="black", weight="bold"), style.fill(color="lightgray")],
            locations=loc.row_groups(),
        )
    )
    html_data.append(gt.as_raw_html())

    # --- Table 9a: Primary Endpoint met -------------------------------------
    df_endpoint_grp = (
        df_endpoint.groupby(by=["site_id", "endpoint_label"]).size().to_frame().reset_index()
    )
    df_endpoint_grp.columns = ["site_id", "label", "endpoints"]
    df_endpoint_pivot = df_endpoint_grp.pivot_table(
        index="label", columns="site_id", values="endpoints"
    ).reset_index()
    df_endpoint_pivot.columns.name = ""
    df_endpoint_pivot.columns = ["label", "10", "20", "30", "40", "60"]
    df_endpoint_pivot.loc[len(df_endpoint_pivot)] = (
        df_endpoint_pivot[["10", "20", "30", "40", "60"]].sum().to_dict()
    )
    df_endpoint_pivot.at[len(df_endpoint_pivot) - 1, "label"] = "Total"
    df_endpoint_pivot["total"] = df_endpoint_pivot[["10", "20", "30", "40", "60"]].sum(axis=1)
    df_endpoint_pivot = df_endpoint_pivot.fillna(0.0)
    gt = df_as_great_table(df_endpoint_pivot, title="Table 9a: Primary Endpoint met")
    gt = (
        gt.cols_label({k: v for k, v in COLUMN_HEADERS.items() if k != "visit_code"})
        .cols_align(align="center", columns=["10", "20", "30", "40", "60", "total"])
        .cols_align(align="left", columns=["label"])
        .cols_width(cases={"label": "25%"})
    )
    html_data.append(gt.as_raw_html())

    # --- Table 9b: Primary Endpoint -- participant not referred -------------
    df_subjecthistory = read_frame(
        SubjectScheduleHistory.objects.filter(
            offschedule_model="meta_prn.offschedule", offschedule_datetime__isnull=False
        ),
        verbose=False,
    ).rename(columns={"site": "site_id"})
    df_subjecthistory["site_id"] = df_subjecthistory["site_id"].astype(str)
    df_endpoint_no_off = df_endpoint.merge(
        df_subjecthistory[["subject_identifier", "offschedule_datetime"]],
        on=["subject_identifier"],
        how="left",
    )
    df_endpoint_grp = (
        df_endpoint_no_off.query("offschedule_datetime.isna()")
        .groupby(by=["site_id", "endpoint_label"])
        .size()
        .to_frame()
        .reset_index()
    )
    df_endpoint_grp.columns = ["site_id", "label", "endpoints"]
    df_endpoint_pivot = df_endpoint_grp.pivot_table(
        index="label", columns="site_id", values="endpoints"
    ).reset_index()
    df_endpoint_pivot.columns.name = ""
    df_endpoint_pivot.columns = [
        "label",
        *[str(col) for col in df_endpoint_pivot.columns if col != "label"],
    ]
    for col in [
        c
        for c in ["label", "10", "20", "30", "40", "60"]
        if str(c) not in df_endpoint_pivot.columns
    ]:
        df_endpoint_pivot[str(col)] = np.nan
    df_endpoint_pivot.columns = ["label", "10", "20", "30", "40", "60"]
    df_endpoint_pivot.loc[len(df_endpoint_pivot)] = (
        df_endpoint_pivot[["10", "20", "30", "40", "60"]].sum().to_dict()
    )
    df_endpoint_pivot.at[len(df_endpoint_pivot) - 1, "label"] = "Total"
    df_endpoint_pivot["total"] = df_endpoint_pivot[["10", "20", "30", "40", "60"]].sum(axis=1)
    df_endpoint_pivot = df_endpoint_pivot.fillna(0.0)
    unreferred_subjects = df_endpoint_no_off.query(
        "offschedule_datetime.isna()"
    ).subject_identifier.to_list()
    gt = df_as_great_table(
        df_endpoint_pivot,
        title="Table 9b: Primary Endpoint met -- participant not referred",
    )
    gt = (
        gt.cols_label({k: v for k, v in COLUMN_HEADERS.items() if k != "visit_code"})
        .cols_align(align="center", columns=["10", "20", "30", "40", "60", "total"])
        .cols_align(align="left", columns=["label"])
        .cols_width(cases={"label": "25%"})
        .tab_source_note(source_note=html("<BR>".join(unreferred_subjects)))
    )
    html_data.append(gt.as_raw_html())

    # --- Table 10/11: incidence and proportion ------------------------------
    incidence_data: dict[str, list] = {}
    for term, lower, upper in [
        ("total", -1, 10000),
        ("0-1 years", -1, 365.25),
        ("1-2 years", 365.25, 2 * 365.25),
        ("2-3 years", 2 * 365.25, 3 * 365.25),
        ("3+ years", 3 * 365.25, 10 * 365.25),
    ]:
        incidence_data.update(_get_incidence_data(df_visit, df_endpoint, term, lower, upper))
    data = dict(
        label=[],
        person_years=[],
        subjects=[],
        failures=[],
        rate=[],
        lower_ci=[],
        upper_ci=[],
    )
    for k, v in incidence_data.items():
        data["label"].append(k)
        data["person_years"].append(v[0])
        data["subjects"].append(v[1])
        data["failures"].append(v[2])
        data["rate"].append(v[3])
        data["lower_ci"].append(v[4])
        data["upper_ci"].append(v[5])

    df_table_10 = pd.DataFrame(data={k: v for k, v in data.items() if k != "subjects"})
    gt = df_as_great_table(
        df_table_10,
        title="Table 10: Incident Rate per 1000 person years",
        subtitle=md("using randomisation to diabetes/last seen"),
    )
    gt = gt.fmt_number(
        columns=["person_years", "failures", "rate", "lower_ci", "upper_ci"], decimals=2
    )
    gt = (
        gt.cols_label(
            {
                "label": "Label",
                "person_years": "Person years",
                "failures": "Failures",
                "rate": "Rate",
                "lower_ci": "Lower",
                "upper_ci": "Upper",
            }
        )
        .cols_align(align="left", columns=["label"])
        .cols_align(
            align="center",
            columns=["person_years", "failures", "rate", "lower_ci", "upper_ci"],
        )
        .tab_spanner(label="95%CI", columns=["lower_ci", "upper_ci"])
        .tab_source_note(
            source_note="Excluding patients withdrawn for `late exclusion` criteria"
        )
    )
    html_data.append(gt.as_raw_html())

    df_table_11 = pd.DataFrame(data=data)
    df_table_11["proportion"] = df_table_11["failures"] / df_table_11["subjects"] * 100
    gt = df_as_great_table(
        df_table_11[["label", "subjects", "failures", "proportion"]],
        title="Table 11: Proportion meeting primary endpoint",
    )
    gt = (
        gt.fmt_number(columns=["failures", "proportion"], decimals=2)
        .cols_label(
            {
                "label": "Label",
                "subjects": "Participants",
                "failures": "Failures",
                "proportion": "%",
            }
        )
        .cols_align(align="left", columns=["label"])
        .cols_align(align="center", columns=["subjects", "failures", "proportion"])
        .tab_source_note(
            source_note="Excluding patients withdrawn for `late exclusion` criteria"
        )
    )
    html_data.append(gt.as_raw_html())

    # --- Table 12a: End of Study --------------------------------------------
    df_eos = get_eos_df()
    df_eos_1691 = df_eos.copy()
    offstudy_reasons_map = {
        "Delivered / Completed followup from pregnancy": "Pregnancy",
        "Patient completed 48 months of follow-up": "Completed 48m",
        "Patient completed 36 months of follow-up": "Completed 36m",
        "Patient developed diabetes": "Developed diabetes",
        "Other reason (specify below)": "Other",
        LATE_EXCLUSION_REASON: "Late exclusion",
        "Patient has been transferred to another health centre": "Transferred out",
        "Patient is withdrawn on CLINICAL grounds ...": "Withdrawal: Clinical grounds",
        "Patient lost to follow-up": "LTFU",
        "Patient reported/known to have died": "Died",
        "Patient withdrew consent to participate further": "Withdrawal: Consent",
    }
    df_eos["offstudy_reason"] = df_eos["offstudy_reason"].map(offstudy_reasons_map)
    df_eos["offstudy_reason"] = pd.Categorical(
        df_eos["offstudy_reason"],
        categories=sorted(list(offstudy_reasons_map.values())),
        ordered=True,
    )
    df_eos["site_id"] = df_eos["site_id"].astype(str)
    df_eos_pivot = (
        df_eos.groupby(by=["offstudy_reason", "site_id"], observed=True)
        .size()
        .reset_index()
        .pivot_table(index="offstudy_reason", columns="site_id", values=0, observed=True)
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    df_eos_pivot["total"] = df_eos_pivot[["10", "20", "30", "40", "60"]].sum(axis=1)
    df_eos_pivot.columns.name = ""
    sum_row = df_eos_pivot.select_dtypes(include="int64").sum()
    sum_row["offstudy_reason"] = "Total"
    sum_row_df = pd.DataFrame(sum_row).T
    enrolled_1691_pivot["offstudy_reason"] = "Enrolled"
    enrolled_1691_pivot = enrolled_1691_pivot[[*df_eos_pivot.columns]]
    df_eos_pivot = pd.concat(
        [enrolled_1691_pivot, df_eos_pivot, sum_row_df], ignore_index=True
    )
    gt = df_as_great_table(
        df_eos_pivot,
        title="Table 12a: End of study report",
        subtitle=md("for those who have completed an End of study report"),
    )
    gt = (
        gt.cols_label(
            {
                "offstudy_reason": "Reason",
                **{
                    k: v for k, v in COLUMN_HEADERS.items() if k not in ["visit_code", "label"]
                },
            }
        )
        .cols_align(align="left", columns=["offstudy_reason"])
        .cols_align(align="center", columns=["10", "20", "30", "40", "60", "total"])
        .tab_style(
            style=[style.fill(color="snow"), style.text(color="black")],
            locations=loc.body(columns=[0], rows=[len(df_eos_pivot) - 1]),
        )
        .tab_style(
            style=[style.fill(color="lightblue"), style.text(color="black")],
            locations=loc.body(
                columns=["10", "20", "30", "40", "60"],
                rows=[len(df_eos_pivot) - 1],
            ),
        )
        .tab_style(
            style=[style.fill(color="lightgreen"), style.text(color="black")],
            locations=loc.body(columns=["total"], rows=[len(df_eos_pivot) - 1]),
        )
        .tab_style(
            style=[style.fill(color="snow"), style.text(color="black")],
            locations=loc.body(columns=["offstudy_reason"], rows=[0]),
        )
    )
    html_data.append(gt.as_raw_html())

    # --- Table 12b: Study status --------------------------------------------
    df_sh = read_frame(SubjectScheduleHistory.objects.all(), verbose=False).rename(
        columns={"site": "site_id"}
    )
    df_sh["site_id"] = df_sh["site_id"].astype(str)
    df_on = (
        pd.concat(
            [
                _get_schedule_df(df_sh, "meta_prn.onschedule", "meta_prn.offschedule", "on"),
                _get_schedule_df(
                    df_sh,
                    "meta_prn.onscheduledmreferral",
                    "meta_prn.offscheduledmreferral",
                    "on",
                ),
                _get_schedule_df(
                    df_sh,
                    "meta_prn.onschedulepregnancy",
                    "meta_prn.offschedulepregnancy",
                    "on",
                ),
            ]
        )
        .fillna(0)
        .reset_index(drop=True)
    )
    df_off = (
        pd.concat(
            [
                _get_schedule_df(df_sh, "meta_prn.onschedule", "meta_prn.offschedule", "off"),
                _get_schedule_df(
                    df_sh,
                    "meta_prn.onscheduledmreferral",
                    "meta_prn.offscheduledmreferral",
                    "off",
                ),
                _get_schedule_df(
                    df_sh,
                    "meta_prn.onschedulepregnancy",
                    "meta_prn.offschedulepregnancy",
                    "off",
                ),
            ]
        )
        .fillna(0)
        .reset_index(drop=True)
    )

    df_status = pd.merge(df_on, df_off, on=["schedule"], how="outer")
    status_cols = []
    for ele in [[f"{x}_on", f"{x}_off"] for x in ["10", "20", "30", "40", "60"]]:
        status_cols.extend(ele)
    df_status = df_status[["schedule", *status_cols]]
    df_status["total_on"] = df_status[[c for c in status_cols if "on" in c]].sum(axis=1)
    df_status["total_off"] = df_status[[c for c in status_cols if "off" in c]].sum(axis=1)
    df_status["total"] = df_status[status_cols].sum(axis=1)
    df_status["schedule"] = df_status.schedule.map(
        {
            "meta_prn.onschedule": "Main trial",
            "meta_prn.onscheduledmreferral": "Diabetes",
            "meta_prn.onschedulepregnancy": "Pregnancy",
        }
    )
    gt = df_as_great_table(
        df_status,
        title="Table 12b: Study status",
        subtitle=md("Calculated from Offschedule form; not End of study report"),
    )
    gt = (
        gt.tab_source_note(
            source_note=(
                "Note: Offschedule form is always submitted before the End of study "
                "report. When the Offschedule form is submitted, future appointments "
                "for the schedule are removed and the site staff are actioned to "
                "submit the End of study report."
            )
        )
        .cols_label(
            {
                "10_on": "On",
                "10_off": "Off",
                "20_on": "On",
                "20_off": "Off",
                "30_on": "On",
                "30_off": "Off",
                "40_on": "On",
                "40_off": "Off",
                "60_on": "On",
                "60_off": "Off",
                "total_on": "On",
                "total_off": "Off",
                "schedule": "Schedule",
                "total": "Total",
            }
        )
        .cols_align(align="center")
        .cols_align(align="left", columns=["schedule"])
        .tab_spanner(label="Hindu mandal", columns=["10_on", "10_off"])
        .tab_spanner(label="Amana", columns=["20_on", "20_off"])
        .tab_spanner(label="Temeke", columns=["30_on", "30_off"])
        .tab_spanner(label="Mwananyamala", columns=["40_on", "40_off"])
        .tab_spanner(label="Mnazi Moja", columns=["60_on", "60_off"])
        .tab_spanner(label="Total", columns=["total_on", "total_off"])
        .tab_style(
            style=[style.fill(color="lightblue"), style.text(color="black")],
            locations=loc.body(
                columns=["10_off", "20_off", "30_off", "40_off", "60_off"],
                rows=list(range(0, 1)),
            ),
        )
        .tab_style(
            style=[style.fill(color="lightgreen"), style.text(color="black")],
            locations=loc.body(columns=["total_off"], rows=list(range(0, 1))),
        )
        .fmt_number(
            columns=[c for c in df_status.columns if c not in ["schedule"]], decimals=0
        )
    )
    html_data.append(gt.as_raw_html())

    # --- Table 13c: EOS report not submitted --------------------------------
    df_eos_submitted = df_eos_pivot.query("offstudy_reason=='Total'")[
        ["10", "20", "30", "40", "60"]
    ].reset_index(drop=True)
    df_off_mainschedule = (
        df_status.query("schedule=='Main trial'")[[c for c in status_cols if "off" in c]]
        .rename(
            columns=dict(
                zip(
                    [c for c in status_cols if "off" in c],
                    ["10", "20", "30", "40", "60"],
                    strict=False,
                )
            )
        )
        .reset_index(drop=True)
    )
    df_eos_not_reported = df_off_mainschedule - df_eos_submitted
    df_eos_not_reported["schedule"] = "Main trial"
    df_eos_not_reported["total"] = df_eos_not_reported[["10", "20", "30", "40", "60"]].sum(
        axis=1
    )
    df_eos_not_reported = df_eos_not_reported[
        ["schedule", "10", "20", "30", "40", "60", "total"]
    ]
    gt = df_as_great_table(
        df_eos_not_reported,
        title="Table 13c: End of study report not submitted",
        subtitle=md("End of study report expected based on Offschedule form"),
    )
    gt = (
        gt.cols_label(
            {
                "schedule": "Schedule",
                **{
                    k: v for k, v in COLUMN_HEADERS.items() if k not in ["visit_code", "label"]
                },
            }
        )
        .cols_align(align="left", columns=["schedule"])
        .cols_align(align="center", columns=["10", "20", "30", "40", "60", "total"])
    )
    html_data.append(gt.as_raw_html())

    # --- Table 15: Consented to extended followup ---------------------------
    df_consented = (
        read_frame(SubjectConsentV1Ext.objects.all(), verbose=False)
        .query("agrees_to_extension==@YES")
        .rename(columns={"site": "site_id"})
    )
    if not df_consented.empty:
        df_consented["site_id"] = df_consented.site_id.astype(str)
        df_consented["month"] = df_consented.report_datetime.dt.strftime("%m")
        df_consented["year"] = df_consented.report_datetime.dt.strftime("%Y")
        df_consented_grp = (
            df_consented.groupby(by=["site_id", "year", "month"])
            .size()
            .reset_index()
            .sort_values(by=["site_id", "year", "month"], ascending=True)
            .reset_index(drop=True)
        )
        df_consented_pivot = (
            df_consented_grp.pivot_table(
                index=["year", "month"], columns="site_id", values=0, aggfunc="sum"
            )
            .reset_index()
            .fillna(0)
        )
        for site in ["10", "20", "30", "40", "60"]:
            if site not in df_consented_pivot.columns:
                df_consented_pivot[site] = 0.0
        df_consented_pivot.columns.name = ""
        df_consented_pivot["year"] = df_consented_pivot["year"].astype(str)
        df_consented_pivot["month"] = df_consented_pivot["month"].astype(str)
        sum_row = df_consented_pivot[["10", "20", "30", "40", "60"]].sum()
        sum_row["year"] = "Total"
        sum_row["month"] = ""
        df_consented_pivot = pd.concat(
            [df_consented_pivot, sum_row.to_frame().T], ignore_index=True
        )
        df_consented_pivot["total"] = (
            df_consented_pivot[["10", "20", "30", "40", "60"]].sum(axis=1).astype(int)
        )
        df_consented_pivot[["10", "20", "30", "40", "60"]] = df_consented_pivot[
            ["10", "20", "30", "40", "60"]
        ].astype(int)
        gt = df_as_great_table2(
            df_consented_pivot,
            title="Table 15: Consented to extended followup",
            rowname_col="month",
            groupname_col="year",
        )
        gt = (
            gt.cols_label(
                {
                    "year": "Year",
                    "month": "Month",
                    **{
                        k: v
                        for k, v in COLUMN_HEADERS.items()
                        if k not in ["visit_code", "label"]
                    },
                }
            )
            .cols_align(align="center")
            .fmt_number(columns=["10", "20", "30", "40", "60", "total"], decimals=0)
            .tab_stubhead(label="Consented")
            .tab_style(
                style=[
                    style.text(color="black", weight="bold"),
                    style.fill(color="lightgray"),
                ],
                locations=loc.row_groups(),
            )
        )
        html_data.append(gt.as_raw_html())

    # also reference so linters don't flag as unused
    _ = df_eos_1691

    # --- assemble and render PDF --------------------------------------------
    raw_html = [f'<div class="page-break">{s}</div>' for s in html_data]
    # WeasyPrint uses @page rules for margins, headers and footers.
    # Study title in @top-center (escape double quotes for CSS string).
    study_title_css = study_title.replace('"', '\\"')
    style_css = f"""
<style>
  @page {{
    size: A4;
    margin: 15mm 15mm 15mm 15mm;
    @top-center {{
      content: "{study_title_css}";
      font-size: 8pt;
    }}
    @bottom-center {{
      content: "Page " counter(page) " of " counter(pages);
      font-size: 8pt;
    }}
  }}
  .page-break {{
    page-break-inside: avoid;
  }}
  .table-header {{
    font-weight: bold;
    font-size: 18px;
    text-align: center;
    border-bottom: none;
  }}
</style>
"""
    raw_html_str = (
        f'<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        f"{style_css}\n</head>\n<body>\n"
        + document_title
        + "".join(raw_html)
        + "\n</body>\n</html>\n"
    )

    # WeasyPrint has no "verbose" option; the flag is accepted for API parity.
    _ = verbose
    HTML(string=raw_html_str).write_pdf(str(output_path))
    return output_path
