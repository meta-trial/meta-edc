part_one_fields = (
    "screening_consent",
    "selection_method",
    "report_datetime",
    "hospital_identifier",
    "initials",
    "gender",
    "age_in_years",
    "ethnicity",
    "hiv_pos",
    "art_six_months",
    "on_rx_stable",
    "lives_nearby",
    "staying_nearby",
    "pregnant",
    "continue_part_two",
)

part_two_fields = (
    "part_two_report_datetime",
    "congestive_heart_failure",
    "liver_disease",
    "alcoholism",
    "acute_metabolic_acidosis",
    "renal_function_condition",
    "tissue_hypoxia_condition",
    "acute_condition",
    "metformin_sensitivity",
    "already_fasted",
    "advised_to_fast",
    "appt_datetime",
)


part_three_vitals_fields = (
    "height",
    "weight",
    "waist_circumference",
    "sys_blood_pressure",
    "dia_blood_pressure",
)

part_three_ifg_fields = (
    "fasting",
    "fasting_duration_str",
    "ifg_datetime",
    "ifg_value",
    "ifg_units",
)

part_three_ogtt_fields = (
    "ogtt_base_datetime",
    "ogtt_datetime",
    "ogtt_value",
    "ogtt_units",
)

part_three_glucose_fields = part_three_ifg_fields + part_three_ogtt_fields

part_three_pregnancy_fields = (
    "urine_bhcg_performed",
    "urine_bhcg_value",
    "urine_bhcg_date",
)

part_three_other_fields = (
    "creatinine_performed",
    "creatinine_value",
    "creatinine_units",
    "hba1c_performed",
    "hba1c_value",
)

part_three_comment_fields = (
    "unsuitable_for_study",
    "reasons_unsuitable",
    "unsuitable_agreed",
)

part_three_fields = (
    *part_three_ifg_fields,
    *part_three_ogtt_fields,
    *part_three_other_fields,
    *part_three_vitals_fields,
    *part_three_pregnancy_fields,
    *part_three_comment_fields,
)


calculated_fields = (
    "calculated_bmi_value",
    "converted_ifg_value",
    "converted_ogtt_value",
    "converted_creatinine_value",
    "calculated_egfr_value",
    "inclusion_a",
    "inclusion_b",
    "inclusion_c",
    "inclusion_d",
)
