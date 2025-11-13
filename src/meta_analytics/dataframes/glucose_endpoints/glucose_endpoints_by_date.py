import numpy as np
import pandas as pd
from clinicedc_constants import NULL_STRING, YES
from django.apps import apps as django_apps
from django.utils import timezone

from ..constants import (
    CASE_EOS,
    CASE_FBG_VERY_HIGH,
    CASE_FBGS_WITH_FIRST_OGTT,
    CASE_FBGS_WITH_SECOND_OGTT,
    CASE_OGTT,
    FBG_BEYOND_THRESHOLD,
    endpoint_cases,
    endpoint_columns,
)
from ..get_glucose_df import get_glucose_df
from ..utils import (
    get_empty_endpoint_df,
    get_test_string,
    get_unique_subject_identifiers,
)
from .endpoint_by_date import EndpointByDate


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
    fbg_beyond_threshold = FBG_BEYOND_THRESHOLD
    ogtt_threshhold = 11.1
    endpoint_cls = EndpointByDate
    keep_cols = [  # noqa: RUF012
        "fasted",
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
            CASE_FBG_VERY_HIGH,
            CASE_EOS,
        ]
        self.endpoint_cases = {k: v for k, v in endpoint_cases.items() if k in self.case_list}

        self.df = get_glucose_df(subject_identifiers=self.subject_identifiers).copy()

        # label rows by type of glu tests (ones with value)
        self.df["test"] = self.df.apply(get_test_string, axis=1)

        self.df = (
            self.df.query("not (fbg_value.isna() and ogtt_value.isna())")
            .sort_values(by=["subject_identifier", "fbg_datetime"])
            .reset_index(drop=True)
        )
        self.working_df = self.df.copy()
        self.working_df["endpoint"] = 0
        self.endpoint_df = get_empty_endpoint_df()

    def run(self):
        self.process_by_ogtt_only()
        self.process_by_fbg_only()
        subject_identifiers_df = get_unique_subject_identifiers(self.df)
        for _, row in subject_identifiers_df.iterrows():
            subject_df = self.endpoint_cls(
                subject_df=self.get_subject_df(row["subject_identifier"]),
                fbg_threshhold=self.fbg_threshhold,
                ogtt_threshhold=self.ogtt_threshhold,
            ).subject_df
            if len(subject_df.loc[subject_df["endpoint"] == 1]) == 1:
                self.append_subject_to_endpoint_df(subject_df)
                self.remove_subject_from_working_df(row)
        self.post_check_endpoint()
        self.merge_with_final_endpoints()

    def process_by_fbg_only(self):
        """Flag subjects that meta endpoint by hitting the absurd FBG"""
        subject_endpoint_df = self.working_df.loc[
            (self.working_df["fbg_value"] >= self.fbg_beyond_threshold)
            # & (self.working_df["fasted"] == YES)
        ].copy()

        subject_endpoint_df = (
            subject_endpoint_df.sort_values(by=["subject_identifier", "fbg_datetime"])
            .reset_index(drop=True)
            .drop_duplicates(subset=["subject_identifier"], keep="first")
            .reset_index(drop=True)
        )
        if not subject_endpoint_df.empty:
            # flag the selected endpoint rows as endpoints
            subject_endpoint_df["endpoint"] = 1
            subject_endpoint_df["endpoint_label"] = self.endpoint_cases[CASE_FBG_VERY_HIGH]
            subject_endpoint_df["endpoint_type"] = CASE_FBG_VERY_HIGH
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

    def process_by_ogtt_only(self):
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
            & (self.working_df["ogtt_value"] <= 9999.99)
            & (self.working_df["fasted"] == YES)
            & (self.working_df["fbg_value"].notna())
        ].copy()

        subject_endpoint_df = (
            subject_endpoint_df.sort_values(by=["subject_identifier", "fbg_datetime"])
            .reset_index(drop=True)
            .drop_duplicates(subset=["subject_identifier"], keep="first")
            .reset_index(drop=True)
        )
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
            ).reset_index(drop=True)

    def remove_subject_from_working_df(self, row: pd.Series) -> None:
        """Removes one subject from the working DF given a Series with
        value `subject_identifier`.
        """
        self.working_df = self.working_df.drop(
            index=self.working_df[
                self.working_df["subject_identifier"] == row["subject_identifier"]
            ].index
        ).reset_index(drop=True)

    def remove_subjects_from_working_df(self, rows: pd.DataFrame) -> None:
        """Removes subjects from the working DF given a DF with
        column `subject_identifier`.
        """
        self.working_df = self.working_df.drop(
            index=self.working_df.loc[
                self.working_df["subject_identifier"].isin(rows["subject_identifier"])
            ].index
        ).reset_index(drop=True)

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
        subject_df[[col for col in subject_df if "value" in col]] = subject_df[
            [col for col in subject_df if "value" in col]
        ].fillna(0.0)

        return subject_df.reset_index(drop=True)

    def check_endpoint_by_fbg_for_subject(
        self,
        subject_df: pd.DataFrame,
        case_list: list[int] | None = None,  # noqa: ARG002
    ) -> pd.DataFrame:
        endpoint = self.endpoint_cls(
            subject_df=subject_df,
            fbg_threshhold=self.fbg_threshhold,
            ogtt_threshhold=self.ogtt_threshhold,
        )
        return endpoint.subject_df

    def post_check_endpoint(self):
        """Add any who were taken off study before endpoint guidelines
        were clearly defined.
        """
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

            self.df = self.df.merge(
                self.endpoint_only_df[["subject_identifier", "visit_code", "endpoint"]],
                on=["subject_identifier", "visit_code"],
                how="left",
                suffixes=("", "_y"),
            )
        self.df = self.df.sort_values(by=["subject_identifier", "fbg_datetime"]).reset_index(
            drop=True
        )

    def to_model(self):
        """Write endpoint_only_df to the Endpoints model"""
        df = self.endpoint_only_df
        model = "meta_reports.endpoints"
        now = timezone.now()
        model_cls = django_apps.get_model(model)
        if self.subject_identifiers:
            model_cls.objects.filter(subject_identifier__in=self.subject_identifiers).delete()
            if self.endpoint_only_df.empty:
                df = pd.DataFrame()
            else:
                df = (
                    self.endpoint_only_df[
                        self.endpoint_only_df["subject_identifier"].isin(
                            self.subject_identifiers
                        )
                    ]
                    .copy()
                    .sort_values(by=["subject_identifier"])
                    .reset_index(drop=True)
                )
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
                    fasting=(NULL_STRING if pd.isna(row["fasted"]) else row["fasted"]),
                    endpoint_label=(
                        NULL_STRING
                        if pd.isna(row["endpoint_label"])
                        else row["endpoint_label"]
                    ),
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
