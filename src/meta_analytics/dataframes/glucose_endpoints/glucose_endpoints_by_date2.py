import numpy as np
import pandas as pd
from clinicedc_constants import NULL_STRING, YES
from django.apps import apps as django_apps
from django.utils import timezone
from django_pandas.io import read_frame
from tqdm import tqdm

from meta_prn.constants import DIABETES_DISPLAY
from meta_prn.models import DmReferral

from ..constants import (
    CASE_EOS,
    CASE_FBG_VERY_HIGH,
    CASE_OGTT,
    FBG_BEYOND_THRESHOLD,
    endpoint_cases,
)
from ..get_glucose_df import get_glucose_df
from ..utils import get_test_string
from .endpoint_by_date import EndpointByDate


class GlucoseEndpointsByDateError(Exception):
    pass


class GlucoseEndpointsByDate2:
    """Usage
    cls = GlucoseEndpointsByDate()
    df = cls.endpoint_df.copy()
    """

    fbg_threshold = 7.0
    fbg_beyond_threshold = FBG_BEYOND_THRESHOLD
    ogtt_threshold = 11.1
    min_fasted_hrs = 8.0
    endpoint_cls = EndpointByDate

    def __init__(
        self, subject_identifiers: list[str] | None = None, verbose: bool | None = None
    ):
        self._working_df: pd.DataFrame = pd.DataFrame()
        self._other_endpoints_df: pd.DataFrame = pd.DataFrame()
        self._high_ogtt_df: pd.DataFrame = pd.DataFrame()
        self._high_fbg_df: pd.DataFrame = pd.DataFrame()
        self._eos_df: pd.DataFrame = pd.DataFrame()
        self._dmreferral_df: pd.DataFrame = pd.DataFrame()
        self._endpoint_df: pd.DataFrame = pd.DataFrame()
        self.subject_identifiers = subject_identifiers
        self.verbose = True if verbose is None else verbose
        self.run()

    def run(self):
        return self.endpoint_df

    @property
    def endpoint_df(self):
        if self._endpoint_df.empty:
            self._endpoint_df = pd.concat(
                [self.high_ogtt_df, self.high_fbg_df, self.other_endpoints_df],
                ignore_index=True,
            )
            df_eos = self.eos_df.loc[
                ~(
                    self.eos_df["subject_identifier"].isin(
                        self._endpoint_df.subject_identifier.unique()
                    )
                )
            ]
            self._endpoint_df = pd.concat([self._endpoint_df, df_eos], ignore_index=True)
            self._endpoint_df = (
                self._endpoint_df.sort_values(by=["subject_identifier", "visit_datetime"])
                .reset_index(drop=True)
                .drop_duplicates(subset=["subject_identifier"], keep="first")
                .reset_index(drop=True)
            )
            self._endpoint_df = self._endpoint_df.merge(
                self.dmreferral_df, on="subject_identifier", how="left"
            )
            self._endpoint_df["days_to_event"] = (
                self._endpoint_df["visit_datetime"] - self._endpoint_df["baseline_datetime"]
            ).dt.days
        return self._endpoint_df

    @property
    def working_df(self) -> pd.DataFrame:
        if self._working_df.empty:
            working_df = (
                get_glucose_df(subject_identifiers=self.subject_identifiers)
                .copy()
                .reset_index(drop=True)
            )
            working_df["test"] = working_df.apply(get_test_string, axis=1)
            working_df = working_df.sort_values(
                by=["subject_identifier", "fbg_datetime"]
            ).reset_index(drop=True)
            working_df["endpoint"] = 0
            working_df.loc[working_df.fasted_hrs.isna(), "fasted_hrs"] = self.min_fasted_hrs

            working_df = (
                working_df.loc[
                    ((working_df["ogtt_value"] <= 9999.99) | (working_df["ogtt_value"].isna()))
                    & (working_df["fasted"] == YES)
                    & (working_df["fasted_hrs"] >= self.min_fasted_hrs)
                    & (working_df["fbg_value"].notna())
                ]
                .sort_values(by=["subject_identifier", "visit_datetime"])
                .reset_index(drop=True)
            )
            if (
                len(
                    working_df.loc[
                        ~(working_df["ogtt_units"].isin(["mmol/L (millimoles/L)", "N/A"]))
                        & ~(working_df["ogtt_units"].isna())
                    ]
                )
                > 0
            ):
                raise GlucoseEndpointsByDateError("Check OGTT units")

            if (
                len(
                    working_df.loc[
                        ~(working_df["fbg_units"].isin(["mmol/L (millimoles/L)", "N/A"]))
                        & ~(working_df["fbg_units"].isna())
                    ]
                )
                > 0
            ):
                raise GlucoseEndpointsByDateError("Check FBG units")
            self._working_df = working_df
        return self._working_df

    @property
    def high_ogtt_df(self) -> pd.DataFrame:
        """high OGTTs"""
        if self._high_ogtt_df.empty:
            high_ogtt_df = (
                self.working_df.loc[self.working_df["ogtt_value"] >= self.ogtt_threshold]
                .copy()
                .sort_values(by=["subject_identifier", "ogtt_datetime"])
                .reset_index(drop=True)
                .drop_duplicates(subset=["subject_identifier"], keep="first")
                .reset_index(drop=True)
            )
            high_ogtt_df["days_to_event"] = np.nan
            high_ogtt_df["endpoint"] = 1
            high_ogtt_df["endpoint_label"] = endpoint_cases.get(CASE_OGTT)
            high_ogtt_df["endpoint_type"] = CASE_OGTT
            self._high_ogtt_df = high_ogtt_df
        return self._high_ogtt_df

    @property
    def high_fbg_df(self) -> pd.DataFrame:
        """very high FBGs"""
        if self._high_fbg_df.empty:
            high_fbg_df = (
                self.working_df.loc[
                    (self.working_df["fbg_value"] >= self.fbg_beyond_threshold)
                ]
                .copy()
                .sort_values(by=["subject_identifier", "fbg_datetime"])
                .reset_index(drop=True)
                .drop_duplicates(subset=["subject_identifier"], keep="first")
                .reset_index(drop=True)
            )
            high_fbg_df["days_to_event"] = np.nan
            high_fbg_df["endpoint"] = 1
            high_fbg_df["endpoint_label"] = endpoint_cases.get(CASE_FBG_VERY_HIGH)
            high_fbg_df["endpoint_type"] = CASE_FBG_VERY_HIGH
            self._high_fbg_df = high_fbg_df
        return self._high_fbg_df

    @property
    def other_endpoints_df(self) -> pd.DataFrame:
        if self._other_endpoints_df.empty:
            subject_identifiers = self.working_df.subject_identifier.unique()
            total = len(subject_identifiers)
            frames = []
            for subject_identifier in tqdm(
                subject_identifiers,
                total=total,
                disable=not self.verbose,
            ):
                endpoint_by_date = EndpointByDate(
                    self.working_df.loc[
                        self.working_df.subject_identifier == subject_identifier
                    ],
                    fbg_threshold=self.fbg_threshold,
                    ogtt_threshold=self.ogtt_threshold,
                    min_fasted_hrs=self.min_fasted_hrs,
                )
                endpoint_by_date.evaluate()
                frames.append(endpoint_by_date.subject_df.copy())
            concactenated = pd.concat(frames, ignore_index=True)
            self._other_endpoints_df = concactenated.loc[
                concactenated["endpoint"] == 1
            ].sort_values(by=["subject_identifier", "visit_datetime"])
        return self._other_endpoints_df

    @property
    def eos_df(self) -> pd.DataFrame:
        if self._eos_df.empty:
            df_eos = self.working_df.loc[
                (self.working_df["offstudy_reason"] == DIABETES_DISPLAY)
                # & (self.working_df["referral_id"].isna())
            ].copy()
            df_eos["endpoint"] = 1
            df_eos["endpoint_label"] = endpoint_cases[CASE_EOS]
            df_eos["endpoint_type"] = CASE_EOS
            df_eos["days_to_event"] = np.nan
            self._eos_df = (
                df_eos.sort_values(by=["subject_identifier", "visit_datetime"])
                .reset_index(drop=True)
                .drop_duplicates(subset=["subject_identifier"], keep="last")
                .reset_index(drop=True)
            )
        return self._eos_df

    @property
    def dmreferral_df(self) -> pd.DataFrame:
        if self._dmreferral_df.empty:
            subject_identifiers = self.working_df.subject_identifier.unique()
            self._dmreferral_df = read_frame(
                DmReferral.objects.values("subject_identifier", "referral_date", "id").filter(
                    subject_identifier__in=subject_identifiers
                )
            ).rename(columns={"id": "referral_id"})
        return self._dmreferral_df

    def to_model(self):
        """Write endpoint_df to the Endpoints model"""
        df = self.endpoint_df
        model = "meta_reports.endpoints"
        now = timezone.now()
        model_cls = django_apps.get_model(model)
        if self.subject_identifiers:
            model_cls.objects.filter(subject_identifier__in=self.subject_identifiers).delete()
            if self.endpoint_df.empty:
                df = pd.DataFrame()
            else:
                df = (
                    self.endpoint_df[
                        self.endpoint_df["subject_identifier"].isin(self.subject_identifiers)
                    ]
                    .copy()
                    .sort_values(by=["subject_identifier"])
                    .reset_index(drop=True)
                )
        else:
            model_cls.objects.all().delete()
        created = 0
        if not df.empty:
            if not df["fbg_datetime"].dt.tz:
                df["fbg_datetime"] = df["fbg_datetime"].dt.tz_localize("UTC")
            else:
                df["fbg_datetime"] = df["fbg_datetime"].dt.tz_convert("UTC")
            if not df["baseline_datetime"].dt.tz:
                df["baseline_datetime"] = df["baseline_datetime"].dt.tz_localize("UTC")
            else:
                df["baseline_datetime"] = df["baseline_datetime"].dt.tz_convert("UTC")
            data = [
                model_cls(
                    subject_identifier=row["subject_identifier"],
                    site_id=row["site_id"],
                    baseline_date=(
                        None if pd.isna(row["baseline_datetime"]) else row["baseline_datetime"]
                    ),
                    visit_code=None if pd.isna(row["visit_code"]) else row["visit_code"],
                    fbg_value=(None if pd.isna(row["fbg_value"]) else row["fbg_value"]),
                    ogtt_value=None if pd.isna(row["ogtt_value"]) else row["ogtt_value"],
                    fbg_date=(None if pd.isna(row["fbg_datetime"]) else row["fbg_datetime"]),
                    fasting=(NULL_STRING if pd.isna(row["fasted"]) else row["fasted"]),
                    fasted_hrs=(None if pd.isna(row["fasted_hrs"]) else row["fasted_hrs"]),
                    endpoint_label=(
                        NULL_STRING
                        if pd.isna(row["endpoint_label"])
                        else row["endpoint_label"]
                    ),
                    referral_date=(
                        None if pd.isna(row["referral_date"]) else row["referral_date"]
                    ),
                    referral_id=None if pd.isna(row["referral_id"]) else row["referral_id"],
                    offstudy_date=(
                        None if pd.isna(row["offstudy_datetime"]) else row["offstudy_datetime"]
                    ),
                    offstudy_reason=(
                        NULL_STRING
                        if pd.isna(row["offstudy_reason"])
                        else row["offstudy_reason"]
                    ),
                    report_model=model,
                    created=now,
                )
                for _, row in df.iterrows()
            ]
            created = len(model_cls.objects.bulk_create(data))
        return created
