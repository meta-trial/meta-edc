"""Diagnostic: does the insulin/FBG relationship degrade as assay delay grows?

Degradation is error in the *outcome* (insulin), so the signals to watch are,
in order of usefulness:

  1. resid_sd of log(insulin)        rises with delay  (variable loss)
  2. adj_geomean_insulin             falls with delay  (systematic loss)
  3. pearson_r                       falls with delay  (consequence of 1)
  4. slope of log_insulin ~ log_fbg  roughly UNCHANGED

Point 4 matters: random error in Y does not bias the slope of Y on X, it only
inflates residual variance. Do not read a stable slope as "no degradation".
Do not read r alone either: r also shrinks when a stratum has a narrower
spread of glucose, which is why sd_log_fbg sits next to it in the output.

All inference is CLUSTERED BY SUBJECT. Subjects contributing insulin at more
than one visit make rows non-independent; unclustered SEs are too narrow.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import RegressionResults

# ruff: noqa: T201

Z95 = 1.959963984540054


@dataclass(frozen=True)
class Columns:
    """Column names in the two source frames."""

    subject: str = "subject_identifier"
    insulin_value: str = "insulin_value"
    collected: str = "specimen_collection_datetime"
    assayed: str = "assay_datetime"
    fbg_value: str = "fbg_value"
    fbg_datetime: str = "fbg_datetime"


COLUMNS = Columns()
MIN_STRATUM_N = 10

DEFAULT_BINS: tuple[float, ...] = (-0.001, 1.0, 2.0, 4.0, math.inf)
DEFAULT_LABELS: tuple[str, ...] = ("<1d", "1-<2d", "2-<4d", ">=4d")


def pair_insulin_fbg(
    insulin: pd.DataFrame,
    fbg: pd.DataFrame,
    *,
    cols: Columns = COLUMNS,
    tolerance_days: float = 1.0,
) -> pd.DataFrame:
    """Match each insulin specimen to its nearest FBG within `tolerance_days`.

    Insulin and glucose must come from the same physiological moment for this
    check to mean anything. tolerance_days=0 (same draw only) is safest if your
    data supports it; looser pairing injects real biological variation and
    blunts the diagnostic.
    """
    left = (
        insulin.loc[:, [cols.subject, cols.insulin_value, cols.collected, cols.assayed]]
        .dropna(subset=[cols.subject, cols.collected])
        .sort_values(cols.collected)
        .reset_index(drop=True)
    )
    right = (
        fbg.loc[:, [cols.subject, cols.fbg_value, cols.fbg_datetime]]
        .dropna(subset=[cols.subject, cols.fbg_datetime])
        .sort_values(cols.fbg_datetime)
        .reset_index(drop=True)
    )
    return (
        pd.merge_asof(
            left,
            right,
            left_on=cols.collected,
            right_on=cols.fbg_datetime,
            by=cols.subject,
            direction="nearest",
            tolerance=pd.Timedelta(days=tolerance_days),
        )
        .assign(
            pair_gap_days=lambda d: (
                (d[cols.fbg_datetime] - d[cols.collected]).dt.total_seconds() / 86400.0
            )
        )
        .dropna(subset=[cols.fbg_value])
    )


def add_delay_and_logs(
    paired: pd.DataFrame,
    *,
    cols: Columns = COLUMNS,
    lloq: float | None = None,
    bins: tuple[float, ...] = DEFAULT_BINS,
    labels: tuple[str, ...] = DEFAULT_LABELS,
) -> pd.DataFrame:
    """Add delay_days, log transforms, LLOQ flag and the delay stratum."""
    return (
        paired.assign(
            delay_days=lambda d: (
                (d[cols.assayed] - d[cols.collected]).dt.total_seconds() / 86400.0
            ),
        )
        .loc[lambda d: d["delay_days"].notna() & (d["delay_days"] >= 0)]
        .loc[lambda d: (d[cols.insulin_value] > 0) & (d[cols.fbg_value] > 0)]
        .assign(
            log_insulin=lambda d: np.log(d[cols.insulin_value]),
            log_fbg=lambda d: np.log(d[cols.fbg_value]),
            at_lloq=lambda d: False if lloq is None else d[cols.insulin_value] <= lloq,
            delay_stratum=lambda d: pd.cut(
                d["delay_days"], bins=list(bins), labels=list(labels), right=False
            ),
        )
        .assign(
            log_fbg_c=lambda d: d["log_fbg"] - d["log_fbg"].mean(),
            _cluster=lambda d: d[cols.subject],
        )
    )


def _fit(formula: str, data: pd.DataFrame) -> RegressionResults:
    """OLS with subject-clustered, small-sample-corrected standard errors."""
    return smf.ols(formula, data=data).fit(
        cov_type="cluster",
        cov_kwds={"groups": data["_cluster"]},
        use_t=True,
    )


def stratum_summary(prepared: pd.DataFrame, *, cols: Columns = COLUMNS) -> pd.DataFrame:
    """One row per delay stratum with every quantity worth eyeballing."""
    rows: list[dict[str, object]] = []
    for stratum, block in prepared.groupby("delay_stratum", observed=True):
        n = len(block)
        if n < MIN_STRATUM_N:
            rows.append({"stratum": stratum, "n": n, "note": "too few to model"})
            continue
        fit = _fit("log_insulin ~ log_fbg_c", block)
        intercept_ci = fit.conf_int().loc["Intercept"]
        r = float(np.corrcoef(block["log_insulin"], block["log_fbg_c"])[0, 1])
        zr, se_z = math.atanh(r), 1.0 / math.sqrt(n - 3)
        rows.append(
            {
                "stratum": stratum,
                "n": n,
                "n_subjects": int(block[cols.subject].nunique()),
                "median_delay_d": round(float(block["delay_days"].median()), 2),
                # systematic loss: geometric mean insulin at the grand-mean glucose
                "adj_geomean_insulin": round(math.exp(float(fit.params["Intercept"])), 2),
                "adj_geomean_lcl": round(math.exp(float(intercept_ci.iloc[0])), 2),
                "adj_geomean_ucl": round(math.exp(float(intercept_ci.iloc[1])), 2),
                # variable loss: the primary signal
                "resid_sd": round(math.sqrt(float(fit.mse_resid)), 3),
                # correlation, with its spread-of-X confound alongside it
                "pearson_r": round(r, 3),
                "r_lcl": round(math.tanh(zr - Z95 * se_z), 3),
                "r_ucl": round(math.tanh(zr + Z95 * se_z), 3),
                "sd_log_fbg": round(float(block["log_fbg"].std(ddof=1)), 3),
                # expected to be flat even under real degradation
                "slope": round(float(fit.params["log_fbg_c"]), 3),
                "slope_se": round(float(fit.bse["log_fbg_c"]), 3),
                "pct_at_lloq": round(100.0 * float(block["at_lloq"].mean()), 1),
                "geomean_insulin_raw": round(
                    float(np.exp(np.log(block[cols.insulin_value]).mean())), 2
                ),
            }
        )
    return pd.DataFrame(rows)


def fisher_tests(prepared: pd.DataFrame) -> pd.DataFrame:
    """Compare each stratum's correlation against the shortest-delay stratum.

    Note: this one is NOT cluster-aware. With heavy repeat sampling per subject
    treat its p-values as indicative and lean on the pooled models instead.
    """
    stats: dict[object, tuple[float, int]] = {}
    for stratum, block in prepared.groupby("delay_stratum", observed=True):
        if len(block) >= MIN_STRATUM_N:
            r = float(np.corrcoef(block["log_insulin"], block["log_fbg"])[0, 1])
            stats[stratum] = (math.atanh(r), len(block))
    if not stats:
        return pd.DataFrame()
    ref = next(iter(stats))
    z_ref, n_ref = stats[ref]
    rows = [
        {
            "reference": ref,
            "stratum": stratum,
            "delta_r": round(math.tanh(z_s) - math.tanh(z_ref), 3),
            "z": round(z := (z_ref - z_s) / math.sqrt(1 / (n_ref - 3) + 1 / (n_s - 3)), 2),
            "p_two_sided": round(math.erfc(abs(z) / math.sqrt(2.0)), 4),
        }
        for stratum, (z_s, n_s) in stats.items()
        if stratum != ref
    ]
    return pd.DataFrame(rows)


def pooled_models(
    prepared: pd.DataFrame, *, covariates: list[str] | None = None
) -> tuple[pd.DataFrame, dict[str, RegressionResults]]:
    """Three pooled tests using delay as a continuous variable.

    * level   : log_insulin ~ log_fbg_c + delay   -> systematic loss per day
    * interact: log_insulin ~ log_fbg_c * delay   -> is the slope modified
    * spread  : |resid| ~ delay                   -> does scatter grow (the
                direct test of degradation as added noise in the outcome)

    Pass covariates=["site", "assay_batch"] to adjust; they enter as C(term).
    """
    adjust = "".join(f" + C({name})" for name in covariates or [])
    level = _fit(f"log_insulin ~ log_fbg_c + delay_days{adjust}", prepared)
    interact = _fit(f"log_insulin ~ log_fbg_c * delay_days{adjust}", prepared)

    spread_data = prepared.assign(abs_resid=np.abs(level.resid))
    spread = _fit(f"abs_resid ~ delay_days{adjust}", spread_data)

    fits = {"level": level, "interact": interact, "spread": spread}
    frames = [
        pd.DataFrame(
            {
                "model": name,
                "term": fit.params.index,
                "coef": fit.params.round(4).to_numpy(),
                "lcl": fit.conf_int().iloc[:, 0].round(4).to_numpy(),
                "ucl": fit.conf_int().iloc[:, 1].round(4).to_numpy(),
                "p": fit.pvalues.round(4).to_numpy(),
            }
        )
        for name, fit in fits.items()
    ]
    return pd.concat(frames, ignore_index=True), fits


def interpret(fits: dict[str, RegressionResults]) -> pd.DataFrame:
    """The three headline numbers, on a readable scale."""
    level, interact, spread = fits["level"], fits["interact"], fits["spread"]
    lo, hi = level.conf_int().loc["delay_days"]
    inter_term = next(t for t in interact.params.index if ":" in t)
    return pd.DataFrame(
        [
            {
                "question": "systematic loss per day of delay",
                "estimate": f"{100 * (math.exp(level.params['delay_days']) - 1):+.1f}%",
                "ci": f"{100 * (math.exp(lo) - 1):+.1f}% to {100 * (math.exp(hi) - 1):+.1f}%",
                "p": round(float(level.pvalues["delay_days"]), 4),
            },
            {
                "question": "slope modified by delay (expect no)",
                "estimate": f"{interact.params[inter_term]:+.3f}",
                "ci": "see pooled",
                "p": round(float(interact.pvalues[inter_term]), 4),
            },
            {
                "question": "extra scatter per day of delay",
                "estimate": f"{spread.params['delay_days']:+.4f} log units",
                "ci": "see pooled",
                "p": round(float(spread.pvalues["delay_days"]), 4),
            },
        ]
    )


def run(  # noqa: PLR0913
    insulin: pd.DataFrame,
    fbg: pd.DataFrame,
    *,
    cols: Columns = COLUMNS,
    tolerance_days: float = 1.0,
    lloq: float | None = None,
    covariates: list[str] | None = None,
) -> dict[str, object]:
    """Pair, prepare and run every check."""
    prepared = add_delay_and_logs(
        pair_insulin_fbg(insulin, fbg, cols=cols, tolerance_days=tolerance_days),
        cols=cols,
        lloq=lloq,
    )
    pooled, fits = pooled_models(prepared, covariates=covariates)
    return {
        "prepared": prepared,
        "by_stratum": stratum_summary(prepared, cols=cols),
        "fisher": fisher_tests(prepared),
        "pooled": pooled,
        "headline": interpret(fits),
        "fits": fits,
    }


def _synthetic(
    n_subjects: int = 400,
    visits: int = 3,
    *,
    daily_loss: float = 0.12,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Repeat-measures synthetic data with a KNOWN planted degradation effect.

    Both the systematic loss and the variability of the loss scale with
    daily_loss, so daily_loss=0 is a genuine null control. Subjects get a
    random intercept, which is what makes clustering bite.
    """
    rng = np.random.default_rng(seed)
    n = n_subjects * visits
    subject_effect = np.repeat(rng.normal(0, 0.40, n_subjects), visits)
    fbg_value = np.exp(rng.normal(math.log(5.4), 0.18, n))
    true_insulin = np.exp(1.6 * np.log(fbg_value) + subject_effect + rng.normal(-0.6, 0.30, n))
    delay = rng.choice([0.2, 1.3, 2.6, 5.4], n, p=[0.45, 0.3, 0.15, 0.1])
    observed = true_insulin * np.exp(
        -daily_loss * delay + rng.normal(0, 2.0 * daily_loss * delay, n)
    )
    collected = pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 600, n), unit="D")
    subjects = np.repeat([f"SUBJ-{i:04d}" for i in range(n_subjects)], visits)
    insulin = pd.DataFrame(
        {
            "subject_identifier": subjects,
            "insulin_value": observed,
            "specimen_collection_datetime": collected,
            "assay_datetime": collected + pd.to_timedelta(delay, unit="D"),
        }
    )
    fbg = pd.DataFrame(
        {
            "subject_identifier": subjects,
            "fbg_value": fbg_value,
            "fbg_datetime": collected,
        }
    )
    return insulin, fbg


def _demo(*, daily_loss: float = 0.12) -> None:
    insulin, fbg = _synthetic(daily_loss=daily_loss)
    results = run(insulin, fbg, tolerance_days=0, lloq=2.0)
    print(f"\n=== DEMO (planted daily_loss={daily_loss:.0%}) ===")
    print("\n-- headline --")
    print(results["headline"].to_string(index=False))
    print("\n-- by delay stratum --")
    print(results["by_stratum"].to_string(index=False))
    print("\n-- pooled models --")
    print(results["pooled"].to_string(index=False))

    # what clustering buys: same coef, honest SE
    prepared = results["prepared"]
    naive = smf.ols("log_insulin ~ log_fbg_c + delay_days", data=prepared).fit()
    clustered = results["fits"]["level"]
    print("\n-- delay_days SE: naive vs subject-clustered --")
    print(
        f"   naive      coef={naive.params['delay_days']:+.4f} "
        f"se={naive.bse['delay_days']:.4f}"
    )
    print(
        f"   clustered  coef={clustered.params['delay_days']:+.4f} "
        f"se={clustered.bse['delay_days']:.4f}"
    )


if __name__ == "__main__":
    _demo(daily_loss=0.12)
    _demo(daily_loss=0.0)
