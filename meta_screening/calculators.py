from edc_constants.constants import NO, TBD, YES
from edc_reportable import BMI, MICROMOLES_PER_LITER, eGFR


def calculate_bmi(obj):
    calculated_bmi_value = None
    if obj.height and obj.weight:
        calculated_bmi_value = BMI(height_cm=obj.height, weight_kg=obj.weight).value
    return calculated_bmi_value


def calculate_egfr(obj):
    calculated_egfr_value = None
    if (
        obj.gender
        and obj.age_in_years
        and obj.ethnicity
        and obj.converted_creatinine_value
    ):
        opts = dict(
            gender=obj.gender,
            age=obj.age_in_years,
            ethnicity=obj.ethnicity,
            creatinine_value=obj.converted_creatinine_value,  # umols/L
            creatinine_units=MICROMOLES_PER_LITER,
        )
        calculated_egfr_value = eGFR(**opts).value
    return calculated_egfr_value


def calculate_inclusion_field_values(obj):

    # BMI > 30 combined with IFG (6.1 to 6.9 mmol/L)
    if obj.calculated_bmi_value is None or not obj.converted_ifg_value:
        inclusion_a = TBD
    elif obj.calculated_bmi_value > 30.0 and 6.1 <= obj.converted_ifg_value <= 6.9:
        inclusion_a = YES
    else:
        inclusion_a = NO

    # BMI > 30 combined with OGTT (7.0 to 11.10 mmol/L)
    if obj.calculated_bmi_value is None or not obj.converted_ogtt_value:
        inclusion_b = TBD
    elif obj.calculated_bmi_value > 30.0 and 7.0 <= obj.converted_ogtt_value <= 11.10:
        inclusion_b = YES
    else:
        inclusion_b = NO

    # BMI <= 30 combined with IFG (6.3 to 6.9 mmol/L)
    if obj.calculated_bmi_value is None or not obj.converted_ifg_value:
        inclusion_c = TBD
    elif obj.calculated_bmi_value <= 30.0 and 6.3 <= obj.converted_ifg_value <= 6.9:
        inclusion_c = YES
    else:
        inclusion_c = NO

    # BMI <= 30 combined with OGTT (9.0 to 11.10 mmol/L)
    if obj.calculated_bmi_value is None or not obj.converted_ogtt_value:
        inclusion_d = TBD
    elif obj.calculated_bmi_value <= 30.0 and 9.0 <= obj.converted_ogtt_value <= 11.10:
        inclusion_d = YES
    else:
        inclusion_d = NO

    return inclusion_a, inclusion_b, inclusion_c, inclusion_d
