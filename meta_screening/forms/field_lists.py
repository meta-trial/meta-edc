from meta_edc.meta_version import PHASE_THREE, PHASE_TWO, get_meta_version


def get_part_one_fields():
    fields = [
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
        "staying_nearby_6",
        "pregnant",
        "continue_part_two",
    ]
    if get_meta_version() == PHASE_THREE:
        fields = ["staying_nearby_12" if x == "staying_nearby_6" else x for x in fields]
    return tuple(fields)


def get_part_two_fields():
    fields = [
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
        "advised_to_fast",
        "appt_datetime",
    ]
    if get_meta_version() == PHASE_TWO:
        fields.remove("has_dm")
        fields.remove("on_dm_medication")
    return tuple(fields)


def get_part_three_vitals_fields():
    if get_meta_version() == PHASE_THREE:
        return [
            "height",
            "weight",
            "sys_blood_pressure_one",
            "dia_blood_pressure_one",
            "sys_blood_pressure_two",
            "dia_blood_pressure_two",
            "severe_htn",
        ]
    else:
        return [
            "height",
            "weight",
            "waist_circumference",
            "sys_blood_pressure",
            "dia_blood_pressure",
        ]


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

calculated_fields = (
    "sys_blood_pressure_avg",
    "dia_blood_pressure_avg",
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


# META PHASE_THREE ONLY
part_three_labs = (
    "haemoglobin_value",
    "wbc_value",
    "ast_value",
    "alt_value",
    "alp_value",
    "ggt_value",
    "albumin_value",
)


def get_part_three_fields():
    fields = None
    if get_meta_version() == PHASE_TWO:
        fields = (
            *part_three_ifg_fields,
            *part_three_ogtt_fields,
            *part_three_other_fields,
            *get_part_three_vitals_fields(),
            *part_three_pregnancy_fields,
            *part_three_comment_fields,
        )
    elif get_meta_version() == PHASE_THREE:
        fields = (
            "part_three_report_datetime",
            *get_part_three_vitals_fields(),
            *part_three_pregnancy_fields,
            *part_three_ifg_fields,
            *part_three_ogtt_fields,
            *part_three_other_fields,
            *part_three_comment_fields,
        )
    return fields
