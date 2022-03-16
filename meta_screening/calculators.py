from edc_constants.constants import NO, TBD, YES


def calculate_inclusion_field_values_phase_two(obj):
    # BMI > 30 combined with IFG (6.1 to 6.9 mmol/L)
    if obj.calculated_bmi_value is None or not obj.converted_fbg_value:
        inclusion_a = TBD
    elif obj.calculated_bmi_value > 30.0 and 6.1 <= obj.converted_fbg_value <= 6.9:
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
    if obj.calculated_bmi_value is None or not obj.converted_fbg_value:
        inclusion_c = TBD
    elif obj.calculated_bmi_value <= 30.0 and 6.3 <= obj.converted_fbg_value <= 6.9:
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


def calculate_inclusion_field_values_phase_three(obj):
    converted_ogtt_value = obj.converted_ogtt2_value or obj.converted_ogtt_value
    # IFG (6.1 to 6.9 mmol/L)
    if not obj.converted_fbg_value:
        inclusion_a = TBD
    elif 6.1 <= obj.converted_fbg_value <= 6.9:
        inclusion_a = YES
    else:
        inclusion_a = NO

    # OGTT (7.8 to 11.10 mmol/L)
    if not converted_ogtt_value:
        inclusion_b = TBD
    elif 7.8 <= converted_ogtt_value <= 11.10:
        inclusion_b = YES
    else:
        inclusion_b = NO

    return inclusion_a, inclusion_b
