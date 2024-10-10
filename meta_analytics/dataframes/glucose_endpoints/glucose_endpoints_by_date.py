import numpy as np
import pandas as pd
from django.apps import apps as django_apps
from edc_constants.constants import NO, YES
from edc_pdutils.dataframes import (
    get_crf,
    get_eos,
    get_subject_consent,
    get_subject_visit,
)
from edc_utils import get_utcnow

from ..constants import (
    CASE_EOS,
    CASE_FBG_ONLY,
    CASE_FBGS_WITH_FIRST_OGTT,
    CASE_FBGS_WITH_SECOND_OGTT,
    CASE_OGTT,
    endpoint_cases,
    endpoint_columns,
)
from ..utils import (
    get_empty_endpoint_df,
    get_test_string,
    get_unique_subject_identifiers,
    get_unique_visit_codes,
)
from .endpoint_by_date import EndpointByDate


def calculate_fasting_hrs(df: pd.DataFrame):
    df.loc[(df["fasting"] == NO), "fasting_duration_delta"] = pd.NaT
    if df.empty:
        df["fasting_hrs"] = np.nan
    else:
        df["fasting_hrs"] = df["fasting_duration_delta"].apply(
            lambda s: np.nan if pd.isna(s) else s.total_seconds() / 3600
        )
    return df


class GlucoseEndpointsByDate:
    """
    Usage:
        cls = GlucoseEndpointsByDate()
        cls.run()

        # subjects who reached endpoint
        cls.endpoint_only_df.endpoint_type.value_counts()
        cls.endpoint_only_df.endpoint_label.value_counts()

        # subjects who reached endpoint with total
        result_df = cls.endpoint_only_df.endpoint_label.value_counts().to_frame().reset_index()
        result_df.columns = ["endpoint_label", "total"]
        result_df.loc[-1] = ["total", result_df.total.sum()]
        result_df = result_df.reset_index(drop=True)
        result_df
    """

    fbg_threshhold = 7.0
    ogtt_threshhold = 11.1
    endpoint_cls = EndpointByDate
    keep_cols = [
        "fasting",
        "fasting_hrs",
        "fbg_value",
        "fbg_units",
        "fbg_datetime",
        "ogtt_value",
        "ogtt_units",
        "ogtt_datetime",
        "source",
        "report_datetime",
        "subject_visit_id",
        "subject_identifier",
        "visit_code",
        "visit_datetime",
        "site_id",
        "baseline_datetime",
    ]

    def __init__(
        self, subject_identifiers: list[str] | None = None, case_list: list[int] | None = None
    ):
        self._glucose_fbg_df = pd.DataFrame()
        self._glucose_fbg_ogtt_df = pd.DataFrame()
        self.endpoint_only_df = pd.DataFrame()

        self.subject_identifiers = subject_identifiers or []
        self.case_list = case_list or [
            CASE_OGTT,
            CASE_FBGS_WITH_FIRST_OGTT,
            CASE_FBGS_WITH_SECOND_OGTT,
            CASE_EOS,
        ]
        self.endpoint_cases = {k: v for k, v in endpoint_cases.items() if k in self.case_list}

        # merge two model DFs
        if self.glucose_fbg_ogtt_df.empty:
            self.df = self.glucose_fbg_df.copy()
            self.df[["ogtt_value", "ogtt_units"]] = np.nan
            self.df[["ogtt_datetime"]] = pd.NaT
        elif self.glucose_fbg_df.empty:
            self.df = self.glucose_fbg_ogtt_df.copy()
        else:
            self.df = self.glucose_fbg_ogtt_df.merge(
                self.glucose_fbg_df,
                on=["subject_visit_id"],
                how="outer",
                indicator=True,
                suffixes=("", "_y"),
            )
        # cast as ...
        for col in ["fasting_hrs", "fbg_value"]:
            self.df[col] = self.df[col].astype("float64")
            if f"{col}_y" in self.df.columns:
                self.df[f"{col}_y"] = self.df[f"{col}_y"].astype("float64")
        for col in ["fasting", "fbg_units", "source"]:
            self.df[col] = self.df[col].astype("object")
            if f"{col}_y" in self.df.columns:
                self.df[f"{col}_y"] = self.df[f"{col}_y"].astype("object")
        self.df = self.df.drop(
            columns=[col for col in self.df.columns if col.endswith("_y") or col == "_merge"]
        )
        self.df = self.df.reset_index(drop=True)

        # merge w/ subject_visit
        subject_visit_df = get_subject_visit(
            "meta_subject.subjectvisit", subject_identifiers=self.subject_identifiers
        )
        self.df = subject_visit_df.merge(
            self.df, on=["subject_visit_id"], how="left", suffixes=("", "_y")
        )
        self.df = self.df[[col for col in self.keep_cols]]
        self.df = self.df.reset_index(drop=True)

        # pivot right_only cols
        cols = [
            "fasting",
            "fasting_hrs",
            "fbg_value",
            "fbg_units",
            "fbg_datetime",
            "source",
            "report_datetime",
        ]
        for col in cols:
            if f"{col}_y" in self.df.columns and not self.df[f"{col}_y"].isnull().all():
                self.df.loc[
                    (self.df["_merge"].isin(["both", "right_only"])) & (self.df[col].isna()),
                    col,
                ] = self.df[f"{col}_y"]
        # if fbg_datetime still null, use visit datetime
        if self.df["fbg_datetime"].isnull().all():
            self["fbg_datetime"] = self.df["visit_datetime"]
        else:
            self.df.loc[(self.df["fbg_datetime"].isna()), "fbg_datetime"] = self.df[
                "visit_datetime"
            ]
        self.df = self.df.drop(
            columns=[col for col in self.df.columns if col.endswith("_y") or col == "_merge"]
        )
        self.df = self.df.reset_index(drop=True)

        self.merge_with_consent()
        self.merge_with_eos()

        self.add_calculated_days_from_baseline_to_event_columns()

        # label rows by type of glu tests (ones with value)
        self.df["test"] = self.df.apply(get_test_string, axis=1)
        self.df = self.df.reset_index(drop=True)

        self.visit_codes_df = get_unique_visit_codes(self.df)
        self.subject_identifiers_df = get_unique_subject_identifiers(self.df)

        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df = self.df.reset_index(drop=True)

        self.working_df = self.df.copy()
        self.working_df["endpoint"] = 0
        self.endpoint_df = get_empty_endpoint_df()

    def run(self):
        self.pre_check_endpoint()
        for index, row in self.subject_identifiers_df.iterrows():
            subject_df = self.get_subject_df(row["subject_identifier"])
            subject_df = self.check_endpoint_by_fbg_for_subject(
                subject_df, case_list=[CASE_FBGS_WITH_FIRST_OGTT, CASE_FBGS_WITH_SECOND_OGTT]
            )
            if len(subject_df.loc[subject_df["endpoint"] == 1]) == 1:
                self.append_subject_to_endpoint_df(subject_df)
                self.remove_subject_from_working_df(row)

        if CASE_FBG_ONLY in self.endpoint_cases:
            for index, row in self.subject_identifiers_df.iterrows():
                subject_df = self.get_subject_df(row["subject_identifier"])
                subject_df = self.check_endpoint_by_fbg_for_subject(
                    subject_df, case_list=[CASE_FBG_ONLY]
                )
                if len(subject_df.loc[subject_df["endpoint"] == 1]) == 1:
                    self.append_subject_to_endpoint_df(subject_df)
                    self.remove_subject_from_working_df(row)

        self.post_check_endpoint()
        self.merge_with_final_endpoints()

    @property
    def glucose_fbg_df(self) -> pd.DataFrame:
        """Returns a prepared Dataframe of CRF
        meta_subject.glucosefbg.

        Note: meta_subject.glucosefbg has only FBG measures.
        """
        if self._glucose_fbg_df.empty:
            df = get_crf(
                model="meta_subject.glucosefbg",
                subject_identifiers=self.subject_identifiers,
                # subject_visit_model="meta_subject.subjectvisit",
            )
            df["source"] = "meta_subject.glucosefbg"
            df.rename(columns={"fbg_fasting": "fasting"}, inplace=True)
            df.loc[(df["fasting"] == "fasting"), "fasting"] = YES
            df.loc[(df["fasting"] == "non_fasting"), "fasting"] = NO
            df = calculate_fasting_hrs(df)
            # df = df[[col for col in self.keep_cols if not col.startswith("ogtt")]]
            df = df.reset_index(drop=True)
            self._glucose_fbg_df = df
        return self._glucose_fbg_df

    @property
    def glucose_fbg_ogtt_df(self):
        """Returns a prepared Dataframe of CRF meta_subject.glucose.

        Note: meta_subject.glucose has FBG and OGTT measures.
        """
        if self._glucose_fbg_ogtt_df.empty:
            df = get_crf(
                model="meta_subject.glucose",
                subject_identifiers=self.subject_identifiers,
                # subject_visit_model="meta_subject.subjectvisit",
            )
            df["source"] = "meta_subject.glucose"
            df = calculate_fasting_hrs(df)
            # df = df[self.keep_cols]
            df = df.reset_index(drop=True)
            self._glucose_fbg_ogtt_df = df
        return self._glucose_fbg_ogtt_df

    def merge_with_consent(self):
        """Merge in consent DF."""
        df_consent = get_subject_consent(
            "meta_consent.subjectconsent", subject_identifiers=self.subject_identifiers
        )
        self.df = pd.merge(
            self.df, df_consent, on="subject_identifier", how="left", suffixes=("", "_y")
        )
        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df = self.df.reset_index(drop=True)

    def merge_with_eos(self):
        """Merge in EoS DF.

        Drops patients who were taken off study by late exclusion.
        """
        df_eos = get_eos("meta_prn.endofstudy", subject_identifiers=self.subject_identifiers)
        df_eos = df_eos[
            df_eos["offstudy_reason"]
            != (
                "Patient fulfilled late exclusion criteria (due to abnormal blood "
                "values or raised blood pressure at enrolment"
            )
        ]
        self.df = pd.merge(
            self.df, df_eos, on="subject_identifier", how="left", suffixes=("", "_y")
        )
        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df = self.df.reset_index(drop=True)

    def add_calculated_days_from_baseline_to_event_columns(self):
        """Add columns that calculate number of days from
        baseline to visit, fbg, and ogtt.
        """
        self.df["visit_days"] = np.nan
        self.df["fbg_days"] = np.nan
        self.df["ogtt_days"] = np.nan
        self.df["test"] = np.nan
        self.df["visit_days"] = (
            self.df["visit_datetime"] - self.df["baseline_datetime"]
        ).dt.days
        if not self.df["fbg_datetime"].isnull().all():
            self.df["fbg_days"] = (
                self.df["fbg_datetime"] - self.df["baseline_datetime"]
            ).dt.days
        if not self.df["ogtt_datetime"].isnull().all():
            self.df["ogtt_days"] = (
                self.df["ogtt_datetime"] - self.df["baseline_datetime"]
            ).dt.days
        self.df["visit_days"] = pd.to_numeric(self.df["visit_days"], downcast="integer")
        self.df["fbg_days"] = pd.to_numeric(self.df["fbg_days"], downcast="integer")
        self.df["ogtt_days"] = pd.to_numeric(self.df["ogtt_days"], downcast="integer")
        self.df = self.df.reset_index(drop=True)

    def pre_check_endpoint(self):
        """Flag subjects that met endpoint by hitting the OGTT
        threshold.

        Add them to the endpoint_df and remove them from the
        working_df.

        Subject must have fasted at the timepoint.

        The OGTT must have an FBG measure at the same timepoint.
        The value of the FBG is not considered.

        Most of these where taken off study for the OGTT. We are
        using the OGTT as the reason/date instead of the offstudy
        reason/date.

        See `merge_with_final_endpoints` where we pick the date of
        the first OGTT.
        """
        subject_endpoint_df = self.working_df.loc[
            (self.working_df["ogtt_value"] >= self.ogtt_threshhold)
            & (self.working_df["fasting"] == YES)
            & (self.working_df["fbg_value"].notna())
        ].copy()
        subject_endpoint_df.sort_values(by=["subject_identifier", "fbg_datetime"])
        subject_endpoint_df = subject_endpoint_df.reset_index(drop=True)
        subject_endpoint_df = subject_endpoint_df.drop_duplicates(
            subset=["subject_identifier"], keep="first"
        )
        subject_endpoint_df = subject_endpoint_df.reset_index(drop=True)
        if not subject_endpoint_df.empty:
            # flag the selected endpoint rows as endpoints
            subject_endpoint_df["endpoint"] = 1
            subject_endpoint_df["endpoint_label"] = self.endpoint_cases[CASE_OGTT]
            subject_endpoint_df["endpoint_type"] = CASE_OGTT
            subject_endpoint_df["interval_in_days"] = np.nan

            # add back the others rows for these subjects
            subjects_df = self.working_df.loc[
                (
                    self.working_df["subject_identifier"].isin(
                        subject_endpoint_df["subject_identifier"]
                    )
                    & ~(
                        self.working_df["fbg_datetime"].isin(
                            subject_endpoint_df["fbg_datetime"]
                        )
                    )
                )
            ].copy()
            subjects_df = subjects_df.reset_index(drop=True)
            subjects_df["endpoint"] = np.nan
            subjects_df["endpoint_label"] = None
            subjects_df["endpoint_type"] = None
            subjects_df["interval_in_days"] = np.nan
            subjects_df = pd.concat([subjects_df, subject_endpoint_df])
            subjects_df = subjects_df.reset_index(drop=True)

            self.append_subject_to_endpoint_df(subjects_df[endpoint_columns])
            self.remove_subjects_from_working_df(subjects_df)

    def append_subject_to_endpoint_df(self, subject_df: pd.DataFrame) -> None:
        """Appends all rows of a subject, or subjects, to the
        Endpoints DF.
        """
        if self.endpoint_df.empty:
            self.endpoint_df = subject_df.copy()
        else:
            self.endpoint_df = pd.concat([self.endpoint_df, subject_df])
            self.endpoint_df = self.endpoint_df.sort_values(
                by=["subject_identifier", "visit_code"]
            )
            self.endpoint_df = self.endpoint_df.reset_index(drop=True)

    def remove_subject_from_working_df(self, row: pd.Series) -> None:
        """Removes one subject from the working DF given a Series with
        value `subject_identifier`.
        """
        self.working_df = self.working_df.drop(
            index=self.working_df[
                self.working_df["subject_identifier"] == row["subject_identifier"]
            ].index
        )
        self.working_df = self.working_df.reset_index(drop=True)

    def remove_subjects_from_working_df(self, rows: pd.DataFrame) -> None:
        """Removes subjects from the working DF given a DF with
        column `subject_identifier`.
        """
        self.working_df = self.working_df.drop(
            index=self.working_df.loc[
                self.working_df["subject_identifier"].isin(rows["subject_identifier"])
            ].index
        )
        self.working_df = self.working_df.reset_index(drop=True)

    def get_subject_df(self, subject_identifier: str) -> pd.DataFrame:
        subject_df = self.working_df.loc[
            self.working_df["subject_identifier"] == subject_identifier
        ].copy()
        subject_df["interval_in_days"] = np.nan
        subject_df["endpoint_type"] = None
        subject_df["endpoint_label"] = None
        subject_df["endpoint"] = 0
        subject_df = subject_df[endpoint_columns]
        subject_df = subject_df.sort_values(["subject_identifier", "fbg_datetime"])
        subject_df = subject_df.reset_index(drop=True)
        return subject_df

    def check_endpoint_by_fbg_for_subject(
        self, subject_df: pd.DataFrame, case_list: list[int] | None = None
    ) -> pd.DataFrame:
        case_list = case_list or [2, 3]
        endpoint = self.endpoint_cls(
            subject_df=subject_df,
            fbg_threshhold=self.fbg_threshhold,
            ogtt_threshhold=self.ogtt_threshhold,
            case_list=case_list,
        )
        return endpoint.subject_df

    def post_check_endpoint(self):
        df_eos = self.working_df.loc[
            self.working_df["offstudy_reason"] == "Patient developed diabetes"
        ].copy()
        df_eos["endpoint"] = 1
        df_eos["endpoint_label"] = self.endpoint_cases[CASE_EOS]
        df_eos["endpoint_type"] = CASE_EOS
        df_eos["interval_in_days"] = np.nan
        df_eos = df_eos.reset_index(drop=True)
        self.append_subject_to_endpoint_df(df_eos[endpoint_columns])
        self.working_df = self.working_df.drop(
            index=self.working_df.loc[
                self.working_df["subject_identifier"].isin(df_eos["subject_identifier"])
            ].index
        )

    def merge_with_final_endpoints(self):
        """Merge endpoint_df with original df"""
        if self.endpoint_df.empty:
            self.df = self.df[~(self.df["subject_identifier"].isin(self.subject_identifiers))]
        else:
            self.endpoint_df["test"] = self.endpoint_df.apply(get_test_string, axis=1)
            self.endpoint_df.loc[self.endpoint_df["endpoint"] == 1, "days_to_endpoint"] = (
                self.endpoint_df["fbg_datetime"] - self.endpoint_df["baseline_datetime"]
            ).dt.days

            # Create DF of subjects taken offstudy (EOS) where endpoint==1.
            # Keep the last record for the subject by fbg_datetime.
            df1 = self.endpoint_df.copy()
            df1 = df1[
                (df1["endpoint_type"].isin([CASE_EOS, CASE_OGTT])) & (df1["endpoint"] == 1)
            ]
            df1 = df1.sort_values(["subject_identifier", "fbg_datetime"])
            df1 = df1.reset_index(drop=True)
            df1 = df1.set_index(["subject_identifier"])
            df1 = df1[~df1.index.duplicated(keep="last")]
            df1 = df1.reset_index(drop=False)

            # Create DF of subjects still on-study where endpoint==1.
            # Keep the first record for the subject by fbg_datetime.
            df2 = self.endpoint_df.copy()
            df2 = df2[
                ~(df2["endpoint_type"].isin([CASE_EOS, CASE_OGTT])) & (df2["endpoint"] == 1)
            ]
            df2 = df2.sort_values(["subject_identifier", "fbg_datetime"])
            df2 = df2.reset_index(drop=True)
            df2 = df2.set_index(["subject_identifier"])
            df2 = df2[~df2.index.duplicated(keep="first")]
            df2 = df2.reset_index(drop=False)

            # create new DF with ONE row per subject for those that reached
            # the endpoint (endpoint=1) by merging two DFs above.
            self.endpoint_only_df = pd.concat([df1, df2])
            self.endpoint_only_df = self.endpoint_only_df.reset_index(drop=True)

            self.df = pd.merge(
                self.df,
                self.endpoint_only_df[["subject_identifier", "visit_code", "endpoint"]],
                on=["subject_identifier", "visit_code"],
                how="left",
                suffixes=("", "_y"),
            )
        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"])
        self.df = self.df.reset_index(drop=True)

    def to_model(self):
        """Write endpoint_only_df to the Endpoints model"""
        df = self.endpoint_only_df
        model = "meta_reports.endpoints"
        now = get_utcnow()
        model_cls = django_apps.get_model(model)
        if self.subject_identifiers:
            model_cls.objects.filter(subject_identifier__in=self.subject_identifiers).delete()
        else:
            model_cls.objects.all().delete()
        created = 0
        if not df.empty:
            df["fbg_datetime"] = df["fbg_datetime"].dt.tz_localize("UTC")
            df["baseline_datetime"] = df["baseline_datetime"].dt.tz_localize("UTC")
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
                    fasting=(None if pd.isna(row["fasting"]) else row["fasting"]),
                    endpoint_label=(
                        None if pd.isna(row["endpoint_label"]) else row["endpoint_label"]
                    ),
                    offstudy_date=(
                        None if pd.isna(row["offstudy_datetime"]) else row["offstudy_datetime"]
                    ),
                    offstudy_reason=(
                        None if pd.isna(row["offstudy_reason"]) else row["offstudy_reason"]
                    ),
                    report_model=model,
                    created=now,
                )
                for _, row in df.iterrows()
            ]
            created = len(model_cls.objects.bulk_create(data))
        return created
