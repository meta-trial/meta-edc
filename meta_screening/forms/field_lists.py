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

part_three_glucose_fields = (
    "fasted",
    "fasted_duration_str",
    "fasting_glucose_datetime",
    "fasting_glucose",
    "fasting_glucose_units",
    "ogtt_base_datetime",
    "ogtt_two_hr_datetime",
    "ogtt_two_hr",
    "ogtt_two_hr_units",
)

part_three_pregnancy_fields = ("urine_bhcg_performed", "urine_bhcg", "urine_bhcg_date")

part_three_other_fields = (
    "creatinine_performed",
    "creatinine",
    "creatinine_units",
    "hba1c_performed",
    "hba1c",
)

part_three_comment_fields = (
    "unsuitable_for_study",
    "reasons_unsuitable",
    "unsuitable_agreed",
)

part_three_fields = (
    *part_three_glucose_fields,
    *part_three_other_fields,
    *part_three_vitals_fields,
    *part_three_pregnancy_fields,
    *part_three_comment_fields,
)


calculated_fields = (
    "calculated_bmi",
    "converted_fasting_glucose",
    "converted_ogtt_two_hr",
    "converted_creatinine",
    "calculated_egfr",
    "inclusion_a",
    "inclusion_b",
    "inclusion_c",
    "inclusion_d",
)
