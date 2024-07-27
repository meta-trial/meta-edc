OGTT_THRESHOLD_MET = "OGTT >= 11.1"
EOS_DM_MET = "EOS - Patient developed diabetes"
CASE_EOS = 7

endpoint_columns = [
    "subject_identifier",
    "site",
    "baseline_datetime",
    "visit_datetime",
    "interval_in_days",
    "visit_code",
    "fbg_value",
    "ogtt_value",
    "fbg_datetime",
    "fasting",
    "endpoint_label",
    "endpoint_type",
    "endpoint",
    "offstudy_datetime",
    "offstudy_reason",
]

endpoint_cases = {
    1: OGTT_THRESHOLD_MET,
    2: "FBG >= 7 x 2, first OGTT<=11.1",
    3: "FBG >= 7 x 2, second OGTT<=11.1",
    4: "FBG >= 7 x 2, OGTT not considered (allow missed)",
    CASE_EOS: EOS_DM_MET,
}
