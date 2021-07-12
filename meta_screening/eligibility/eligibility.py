from django.utils.html import format_html
from edc_constants.constants import FEMALE, MALE, NO, TBD, YES
from edc_reportable import MICROMOLES_PER_LITER, MILLIMOLES_PER_LITER, convert_units
from edc_utils.date import get_utcnow
from meta_edc.meta_version import PHASE_THREE, PHASE_TWO, get_meta_version

from ..calculators import (
    calculate_bmi,
    calculate_egfr,
    calculate_inclusion_field_values_phase_three,
    calculate_inclusion_field_values_phase_two,
)
from ..constants import (
    BMI_IFT_OGTT,
    BMI_IFT_OGTT_INCOMPLETE,
    EGFR_LT_45,
    EGFR_NOT_CALCULATED,
    IFT_OGTT,
    IFT_OGTT_INCOMPLETE,
    SEVERE_HTN,
)


class SubjectScreeningEligibilityError(Exception):
    pass


class EligibilityPartOneError(Exception):
    pass


class EligibilityPartTwoError(Exception):
    pass


class EligibilityPartThreeError(Exception):
    pass


def get_part2_required_fields():
    fields = [
        "congestive_heart_failure",
        "liver_disease",
        "alcoholism",
        "acute_metabolic_acidosis",
        "renal_function_condition",
        "tissue_hypoxia_condition",
        "acute_condition",
        "metformin_sensitivity",
    ]
    if get_meta_version() == PHASE_THREE:
        fields.extend(["has_dm", "on_dm_medication"])
    return fields


def check_eligible_final(obj):
    """Updates model instance fields `eligible` and `reasons_ineligible`."""
    reasons_ineligible = []

    if obj.unsuitable_for_study == YES:
        obj.eligible = False
        reasons_ineligible.append("Subject unsuitable")
    else:
        obj.eligible = True if calculate_eligible_final(obj) == YES else False

    if obj.eligible:
        obj.reasons_ineligible = None
    else:
        if obj.reasons_ineligible_part_one:
            reasons_ineligible.append(obj.reasons_ineligible_part_one)
        if obj.reasons_ineligible_part_two:
            reasons_ineligible.append(obj.reasons_ineligible_part_two)
        if obj.reasons_ineligible_part_three:
            reasons_ineligible.append(obj.reasons_ineligible_part_three)
        if reasons_ineligible:
            obj.reasons_ineligible = "|".join(reasons_ineligible)
        else:
            obj.reasons_ineligible = None
    obj.eligibility_datetime = get_utcnow()


def calculate_eligible_final(obj):
    """Returns YES, NO or TBD."""
    eligible_final = NO
    valid_opts = [YES, NO, TBD]
    if any(
        [
            obj.eligible_part_one not in valid_opts,
            obj.eligible_part_two not in valid_opts,
            obj.eligible_part_three not in valid_opts,
        ]
    ):
        opts = [obj.eligible_part_one, obj.eligible_part_two, obj.eligible_part_three]
        raise SubjectScreeningEligibilityError(
            f"Invalid value for eligible. Got {opts}"
        )
    if any(
        [
            obj.eligible_part_one == TBD,
            obj.eligible_part_two == TBD,
            obj.eligible_part_three == TBD,
        ]
    ):
        eligible_final = TBD
    if all(
        [
            obj.eligible_part_one == YES,
            obj.eligible_part_two == YES,
            obj.eligible_part_three == YES,
        ]
    ):
        eligible_final = YES
    return eligible_final


def calculate_eligible_part_one(obj):
    """Updates model instance fields `eligible_part_one`
    and `reasons_ineligible_part_one`.
    """

    obj.eligible_part_one = TBD
    obj.reasons_ineligible_part_one = None

    required_fields = [
        "gender",
        "age_in_years",
        "hiv_pos",
        "art_six_months",
        "on_rx_stable",
        "lives_nearby",
        "staying_nearby_6",
        "pregnant",
    ]
    if get_meta_version() == PHASE_THREE:
        required_fields = [
            "staying_nearby_12" if x == "staying_nearby_6" else x
            for x in required_fields
        ]

    check_for_required_field_values(obj, required_fields, EligibilityPartOneError)

    reasons_ineligible = []
    if obj.gender not in [MALE, FEMALE]:
        reasons_ineligible.append("gender invalid")
    if obj.age_in_years < 18:
        reasons_ineligible.append("age<18")
    if obj.hiv_pos == NO:
        reasons_ineligible.append("not HIV+")
    if obj.art_six_months == NO:
        reasons_ineligible.append("ART<6m")
    if obj.on_rx_stable == NO:
        reasons_ineligible.append("ART not stable")
    if obj.lives_nearby == NO:
        reasons_ineligible.append("Not living nearby")
    if get_meta_version() == PHASE_THREE and obj.staying_nearby_12 == NO:
        reasons_ineligible.append("Unable/Unwilling to stay nearby")
    elif obj.staying_nearby_6 == NO:
        reasons_ineligible.append("Unable/Unwilling to stay nearby")
    if obj.pregnant == YES:
        reasons_ineligible.append("Pregnant (unconfirmed)")
    eligible = NO if reasons_ineligible else YES
    obj.eligible_part_one = eligible
    obj.reasons_ineligible_part_one = "|".join(reasons_ineligible)
    if obj.eligible_part_one == YES or obj.eligible_part_two != TBD:
        obj.continue_part_two = YES


def calculate_eligible_part_two(obj):
    """Updates model instance fields `eligible_part_two`
    and `reasons_ineligible_part_two`.
    """
    obj.eligible_part_two = TBD
    obj.reasons_ineligible_part_two = None

    check_for_required_field_values(
        obj, get_part2_required_fields(), EligibilityPartTwoError
    )

    reasons_ineligible = []

    responses = {}
    for field in get_part2_required_fields():
        responses.update({field: getattr(obj, field)})
    for k, v in responses.items():
        if v == YES:
            reasons_ineligible.append(k.title().replace("_", " "))
    if not reasons_ineligible and obj.advised_to_fast == NO:
        reasons_ineligible.append("Not advised to fast")
    if not reasons_ineligible and not obj.appt_datetime:
        reasons_ineligible.append("Not scheduled for stage 2")
    eligible = NO if reasons_ineligible else YES
    obj.eligible_part_two = eligible
    obj.reasons_ineligible_part_two = "|".join(reasons_ineligible)


def calculate_eligible_part_three(obj):
    """Updates model instance fields `eligible_part_three`
    and `reasons_ineligible_part_three`.
    """
    obj.eligible_part_three = TBD
    obj.reasons_ineligible_part_three = None

    obj.converted_creatinine_value = convert_units(
        obj.creatinine_value,
        units_from=obj.creatinine_units,
        units_to=MICROMOLES_PER_LITER,
    )

    obj.converted_ifg_value = convert_units(
        obj.ifg_value,
        units_from=obj.ifg_units,
        units_to=MILLIMOLES_PER_LITER,
    )

    obj.converted_ogtt_value = convert_units(
        obj.ogtt_value, units_from=obj.ogtt_units, units_to=MILLIMOLES_PER_LITER
    )

    obj.calculated_bmi_value = calculate_bmi(obj)

    if get_meta_version() == PHASE_TWO:
        a, b, c, d = calculate_inclusion_field_values_phase_two(obj)
        obj.inclusion_a = a
        obj.inclusion_b = b
        obj.inclusion_c = c
        obj.inclusion_d = d
        reasons_ineligible = []
        if any(
            [
                obj.inclusion_a == TBD,
                obj.inclusion_b == TBD,
                obj.inclusion_c == TBD,
                obj.inclusion_d == TBD,
            ]
        ):
            reasons_ineligible.append(BMI_IFT_OGTT_INCOMPLETE)
            obj.eligible_part_three = TBD
        if all(
            [
                obj.inclusion_a == NO,
                obj.inclusion_b == NO,
                obj.inclusion_c == NO,
                obj.inclusion_d == NO,
            ]
        ):
            reasons_ineligible.append(BMI_IFT_OGTT)
            obj.eligible_part_three = NO
        if not reasons_ineligible:
            obj.calculated_egfr_value = calculate_egfr(obj)
            if not obj.calculated_egfr_value:
                reasons_ineligible.append(EGFR_NOT_CALCULATED)
                obj.eligible_part_three = TBD
            elif obj.calculated_egfr_value < 45.0:
                reasons_ineligible.append(EGFR_LT_45)
                obj.eligible_part_three = NO

        if not reasons_ineligible:
            obj.eligible_part_three = YES
        elif (
            BMI_IFT_OGTT_INCOMPLETE not in reasons_ineligible
            and EGFR_NOT_CALCULATED not in reasons_ineligible
        ):
            obj.eligible_part_three = NO
        obj.reasons_ineligible_part_three = "|".join(reasons_ineligible)
    elif get_meta_version() == PHASE_THREE:
        a, b = calculate_inclusion_field_values_phase_three(obj)
        obj.inclusion_a = a
        obj.inclusion_b = b
        reasons_ineligible = []
        if any([obj.inclusion_a == TBD, obj.inclusion_b == TBD]):
            reasons_ineligible.append(IFT_OGTT_INCOMPLETE)
            obj.eligible_part_three = TBD
        if all([obj.inclusion_a == NO, obj.inclusion_b == NO]):
            reasons_ineligible.append(IFT_OGTT)
            obj.eligible_part_three = NO
        if obj.severe_htn == YES:
            reasons_ineligible.append(SEVERE_HTN)
        if not reasons_ineligible:
            obj.calculated_egfr_value = calculate_egfr(obj)
            if not obj.calculated_egfr_value:
                reasons_ineligible.append(EGFR_NOT_CALCULATED)
                obj.eligible_part_three = TBD
            elif obj.calculated_egfr_value < 45.0:
                reasons_ineligible.append(EGFR_LT_45)
                obj.eligible_part_three = NO
        if not reasons_ineligible:
            obj.eligible_part_three = YES
        elif (
            IFT_OGTT_INCOMPLETE not in reasons_ineligible
            and EGFR_NOT_CALCULATED not in reasons_ineligible
        ):
            obj.eligible_part_three = NO
        obj.reasons_ineligible_part_three = "|".join(reasons_ineligible)


def format_reasons_ineligible(*str_values):
    reasons = None
    str_values = [x for x in str_values if x is not None]
    if str_values:
        str_values = "".join(str_values)
        reasons = format_html(str_values.replace("|", "<BR>"))
    return reasons


def eligibility_status(obj):
    status_str = (
        f"P1: {obj.eligible_part_one.upper()}<BR>"
        f"P2: {obj.eligible_part_two.upper()}<BR>"
        f"P3: {obj.eligible_part_three.upper()}<BR>"
    )
    display_label = eligibility_display_label(obj)

    if "PENDING" in display_label:
        display_label = f'<font color="orange"><B>{display_label}</B></font>'

    return status_str + display_label


def eligibility_display_label(obj):
    responses = [obj.eligible_part_one, obj.eligible_part_two, obj.eligible_part_three]
    if obj.eligible:
        display_label = "ELIGIBLE"
    elif TBD in responses and NO not in responses:
        if obj.reasons_ineligible == EGFR_NOT_CALCULATED:
            display_label = "PENDING (SCR/eGFR)"
        else:
            display_label = "PENDING"
    elif (
        obj.eligible_part_one == YES
        and obj.eligible_part_two == YES
        and BMI_IFT_OGTT_INCOMPLETE in obj.reasons_ineligible
    ):
        display_label = "PENDING (BMI/IFT/OGTT)"
    elif (
        obj.eligible_part_one == YES
        and obj.eligible_part_two == YES
        and obj.reasons_ineligible == EGFR_NOT_CALCULATED
    ):
        display_label = "PENDING (SCR/eGFR)"
    else:
        display_label = "not eligible"
    return display_label


def check_for_required_field_values(obj=None, required_fields=None, exception_cls=None):
    required_values = [getattr(obj, f) for f in required_fields]
    if not all(required_values):
        missing_values = {
            f: getattr(obj, f) for f in required_fields if not getattr(obj, f)
        }
        raise exception_cls(f"Missing required values. Got {missing_values}")
