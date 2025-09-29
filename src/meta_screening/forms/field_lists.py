part_one_fields: tuple[str, ...] = (
    "report_datetime",
    "screening_consent",
    "meta_phase_two",
    "selection_method",
    "hospital_identifier",
    "initials",
    "gender",
    "age_in_years",
    "ethnicity",
    "site",
    "hiv_pos",
    "art_six_months",
    "on_rx_stable",
    "vl_undetectable",
    "lives_nearby",
    "staying_nearby_12",
    "pregnant",
    "continue_part_two",
)


part_two_fields: tuple[str, ...] = (
    "part_two_report_datetime",
    "congestive_heart_failure",
    "liver_disease",
    "alcoholism",
    "acute_metabolic_acidosis",
    "renal_function_condition",
    "tissue_hypoxia_condition",
    "acute_condition",
    "metformin_sensitivity",
    "has_dm",
    "on_dm_medication",
    "already_fasted",
    "agree_to_p3",
    "advised_to_fast",
    "appt_datetime",
    "contact_number",
)


part_three_vitals_fields: tuple[str, ...] = (
    "height",
    "weight",
    "sys_blood_pressure_one",
    "dia_blood_pressure_one",
    "sys_blood_pressure_two",
    "dia_blood_pressure_two",
    "severe_htn",
)


part_three_fbg_fields: tuple[str, ...] = (
    "fasting",
    "fasting_duration_str",
    "fbg_datetime",
    "fbg_value",
    "fbg_units",
)


part_three_repeat_fbg_fields: tuple[str, ...] = (
    "fbg2_datetime",
    "fbg2_value",
    "fbg2_units",
)

part_three_ogtt_fields: tuple[str, ...] = (
    "ogtt_base_datetime",
    "ogtt_datetime",
    "ogtt_value",
    "ogtt_units",
)

part_three_repeat_ogtt_fields: tuple[str, ...] = (
    "ogtt2_base_datetime",
    "ogtt2_datetime",
    "ogtt2_value",
    "ogtt2_units",
)

part_three_glucose_fields: tuple[str, ...] = (
    *part_three_fbg_fields,
    *part_three_ogtt_fields,
    *("repeat_glucose_opinion", "repeat_appt_datetime", "contact_number"),
)

part_three_pregnancy_fields: tuple[str, ...] = (
    "urine_bhcg_performed",
    "urine_bhcg_value",
    "urine_bhcg_date",
)

part_three_other_fields: tuple[str, ...] = (
    "creatinine_performed",
    "creatinine_value",
    "creatinine_units",
    "hba1c_performed",
    "hba1c_datetime",
    "hba1c_value",
)

part_three_creatinine_fields: tuple[str, ...] = (
    "creatinine_performed",
    "creatinine_value",
    "creatinine_units",
)

part_three_hba1c_fields: tuple[str, ...] = (
    "hba1c_performed",
    "hba1c_datetime",
    "hba1c_value",
)

part_three_comment_fields: tuple[str, ...] = (
    "unsuitable_for_study",
    "reasons_unsuitable",
    "unsuitable_agreed",
)

calculated_fields: tuple[str, ...] = (
    "sys_blood_pressure_avg",
    "dia_blood_pressure_avg",
    "calculated_bmi_value",
    "converted_fbg_value",
    "converted_ogtt_value",
    "converted_fbg2_value",
    "converted_ogtt2_value",
    "converted_creatinine_value",
    "calculated_egfr_value",
    "inclusion_a",
    "inclusion_b",
    "inclusion_c",
    "inclusion_d",
)


part_three_labs: tuple[str, ...] = (
    "haemoglobin_value",
    "wbc_value",
    "ast_value",
    "alt_value",
    "alp_value",
    "ggt_value",
    "albumin_value",
)


part_three_fields: tuple[str, ...] = (
    "part_three_report_datetime",
    *part_three_vitals_fields,
    *part_three_pregnancy_fields,
    *part_three_fbg_fields,
    *part_three_ogtt_fields,
    *part_three_other_fields,
    *part_three_comment_fields,
)
