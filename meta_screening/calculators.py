from edc_reportable import eGFR, BMI, MICROMOLES_PER_LITER
from edc_constants.constants import YES, NO, TBD


def calculate_bmi(obj):
    calculated_bmi = None
    if obj.height and obj.weight:
        calculated_bmi = BMI(height_cm=obj.height, weight_kg=obj.weight).value
    return calculated_bmi


def calculate_egfr(obj):
    calculated_egfr = None
    if obj.gender and obj.age_in_years and obj.ethnicity and obj.converted_creatinine:
        opts = dict(
            gender=obj.gender,
            age=obj.age_in_years,
            ethnicity=obj.ethnicity,
            creatinine=obj.converted_creatinine,  # umols/L
            creatinine_units=MICROMOLES_PER_LITER,
        )
        calculated_egfr = eGFR(**opts).value
    return calculated_egfr


def calculate_inclusion_field_values(obj):
    # BMI>30 combined with impaired fasting glucose (6.1 to 6.9 mmol/L)

    inclusion_a = None
    inclusion_b = None
    inclusion_c = None
    inclusion_d = None

    if obj.calculated_bmi is None or not obj.converted_fasting_glucose:
        inclusion_a = TBD
    elif (
        obj.calculated_bmi > 30.0
        and obj.converted_fasting_glucose >= 6.1
        and obj.converted_fasting_glucose <= 6.9
    ):
        inclusion_a = YES
    else:
        inclusion_a = NO

    # BMI>30 combined with impaired glucose tolerance at
    # 2 hours (7.0 to 11.10 mmol/L)
    if obj.calculated_bmi is None or not obj.converted_ogtt_two_hr:
        inclusion_b = TBD
    elif (
        obj.calculated_bmi > 30.0
        and obj.converted_ogtt_two_hr >= 7.0
        and obj.converted_ogtt_two_hr <= 11.10
    ):
        inclusion_b = YES
    else:
        inclusion_b = NO

    # BMI<=30 combined with impaired fasting glucose (6.3 to 6.9 mmol/L)
    if obj.calculated_bmi is None or not obj.converted_fasting_glucose:
        inclusion_c = TBD
    elif (
        obj.calculated_bmi <= 30.0
        and obj.converted_fasting_glucose >= 6.3
        and obj.converted_fasting_glucose <= 6.9
    ):
        inclusion_c = YES
    else:
        inclusion_c = NO

    # BMI<=30 combined with impaired glucose tolerance at 2 hours
    # (9.0 to 11.10 mmol/L)
    if obj.calculated_bmi is None or not obj.converted_ogtt_two_hr:
        inclusion_d = TBD
    elif (
        obj.calculated_bmi <= 30.0
        and obj.converted_ogtt_two_hr >= 9.0
        and obj.converted_ogtt_two_hr <= 11.10
    ):
        inclusion_d = YES
    else:
        inclusion_d = NO

    return inclusion_a, inclusion_b, inclusion_c, inclusion_d
