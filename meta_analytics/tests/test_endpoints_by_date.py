from datetime import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_constants.constants import YES

from meta_analytics.dataframes import EndpointByDate


class TestEndpointsByDate(TestCase):
    def test_case_one(self):
        def d(m: int, w: int | None = None):
            if w:
                return datetime.now() - relativedelta(months=m, weeks=w)
            return datetime.now() - relativedelta(months=m)

        def append_to(subject_df, endpoint_df):
            if endpoint_df.empty:
                endpoint_df = subject_df.copy()
            elif subject_df.empty:
                pass
            else:
                endpoint_df = pd.concat([endpoint_df, subject_df])
                endpoint_df = self.endpoint_df.sort_values(
                    by=["subject_identifier", "visit_code"]
                )
                endpoint_df.reset_index(drop=True, inplace=True)

        subject_identifier = "101-1"
        data = {
            "subject_identifier": [subject_identifier] * 10,
            "visit_code": [
                1000.0,
                1005.0,
                1010.0,
                1030.0,
                1060.0,
                1090.0,
                1120.0,
                1115.0,
                1118.0,
                1210.0,
            ],
            "fasting": [YES] * 10,
            "fbg_datetime": [
                d(0),
                d(0, 2),
                d(1),
                d(3),
                d(6),
                d(9),
                d(12),
                d(15),
                d(18),
                d(21),
            ],
            "fbg_value": [np.nan, 6.9, 6.9, 7.1, 7.1, 6.4, 7.0, np.nan, 8.1, np.nan],
            "ogtt_value": [
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                7.9,
                np.nan,
            ],
        }

        fbgs = [np.nan, 6.9, 6.9, 7.1, 7.1, 6.4, 7.0, np.nan, 8.1, np.nan]
        ogtts = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 7.9, np.nan]

        fbgs = [np.nan, 6.9, 6.9, 7.1, 7.1, 6.4, 7.0, 8.1, np.nan, np.nan]
        ogtts = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 7.9, np.nan, np.nan]

        data.update(fbg_values=fbgs, ogtt_values=ogtts)
        subject_df = pd.DataFrame(data)
        subject_df["fasting"] = subject_df.apply(
            lambda r: np.nan if pd.isna(r.fbg_value) else r.fbg_value, axis=1
        )
        subject_df["fbg_datetime"] = subject_df.apply(
            lambda r: np.nan if pd.isna(r.fbg_value) else r.fbg_datetime, axis=1
        )

        endpoint_df = pd.DataFrame()
        for index, row in subject_df.iterrows():
            cls = EndpointByDate(index, row, fbg_threshhold=7.0, ogtt_threshhold=11.1)
            append_to(cls.subject_df, endpoint_df)

        endpoint_df
