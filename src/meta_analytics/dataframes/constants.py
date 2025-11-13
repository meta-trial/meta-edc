CASE_EOS = 7
CASE_FBGS_WITH_FIRST_OGTT = 2
CASE_FBGS_WITH_SECOND_OGTT = 3
CASE_FBG_ONLY = 4
CASE_FBG_VERY_HIGH = 5
CASE_OGTT = 1
EOS_DM_MET = "EOS - Patient developed diabetes"
OGTT_THRESHOLD_MET = "OGTT >= 11.1"
FBG_BEYOND_THRESHOLD = 20.0
FBG_THRESHOLD_MET = f"FBG >= {FBG_BEYOND_THRESHOLD}"
endpoint_columns = [
    "subject_identifier",
    "site_id",
    "baseline_datetime",
    "visit_datetime",
    "interval_in_days",
    "visit_code",
    "fbg_value",
    "ogtt_value",
    "fbg_datetime",
    "fasted",
    "endpoint_label",
    "endpoint_type",
    "endpoint",
    "offstudy_datetime",
    "offstudy_reason",
]

endpoint_cases = {
    CASE_OGTT: OGTT_THRESHOLD_MET,
    CASE_FBGS_WITH_FIRST_OGTT: "FBG >= 7 x 2, first OGTT<=11.1",
    CASE_FBGS_WITH_SECOND_OGTT: "FBG >= 7 x 2, second OGTT<=11.1",
    CASE_FBG_ONLY: "FBG >= 7 x 2, OGTT not considered",
    CASE_FBG_VERY_HIGH: FBG_THRESHOLD_MET,
    CASE_EOS: EOS_DM_MET,
}
