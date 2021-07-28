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


def format_reasons_ineligible(*str_values):
    reasons = None
    str_values = [x for x in str_values if x is not None]
    if str_values:
        str_values = "".join(str_values)
        reasons = format_html(str_values.replace("|", "<BR>"))
    return reasons


def check_for_required_field_values(obj=None, required_fields=None, exception_cls=None):
    required_values = [getattr(obj, f) for f in required_fields]
    if not all(required_values):
        missing_values = {
            f: getattr(obj, f) for f in required_fields if not getattr(obj, f)
        }
        raise exception_cls(f"Missing required values. Got {missing_values}")


class Eligibility:
    def __init__(self, obj):
        self.obj = obj

    def check_eligible_final(self):
        """Updates model instance fields `eligible` and
        `reasons_ineligible`.
        """
        reasons_ineligible = []

        if self.obj.unsuitable_for_study == YES:
            self.obj.eligible = False
            reasons_ineligible.append("Subject unsuitable")
        else:
            self.obj.eligible = (
                True if self.calculate_eligible_final() == YES else False
            )

        if self.obj.eligible:
            self.obj.reasons_ineligible = None
        else:
            if self.obj.reasons_ineligible_part_one:
                reasons_ineligible.append(self.obj.reasons_ineligible_part_one)
            if self.obj.reasons_ineligible_part_two:
                reasons_ineligible.append(self.obj.reasons_ineligible_part_two)
            if self.obj.reasons_ineligible_part_three:
                reasons_ineligible.append(self.obj.reasons_ineligible_part_three)
            if reasons_ineligible:
                self.obj.reasons_ineligible = "|".join(reasons_ineligible)
            else:
                self.obj.reasons_ineligible = None
        self.obj.eligibility_datetime = get_utcnow()

    def calculate_eligible_final(self):
        """Returns YES, NO or TBD."""
        eligible_final = NO
        valid_opts = [YES, NO, TBD]
        if any(
            [
                self.obj.eligible_part_one not in valid_opts,
                self.obj.eligible_part_two not in valid_opts,
                self.obj.eligible_part_three not in valid_opts,
            ]
        ):
            opts = [
                self.obj.eligible_part_one,
                self.obj.eligible_part_two,
                self.obj.eligible_part_three,
            ]
            raise SubjectScreeningEligibilityError(
                f"Invalid value for eligible. Got {opts}"
            )
        if any(
            [
                self.obj.eligible_part_one == TBD,
                self.obj.eligible_part_two == TBD,
                self.obj.eligible_part_three == TBD,
            ]
        ):
            eligible_final = TBD
        if all(
            [
                self.obj.eligible_part_one == YES,
                self.obj.eligible_part_two == YES,
                self.obj.eligible_part_three == YES,
            ]
        ):
            eligible_final = YES
        return eligible_final

    def calculate_eligible_part_one(self):
        """Updates model instance fields `eligible_part_one`
        and `reasons_ineligible_part_one`.
        """

        self.obj.eligible_part_one = TBD
        self.obj.reasons_ineligible_part_one = None

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

        check_for_required_field_values(
            self.obj, required_fields, EligibilityPartOneError
        )

        reasons_ineligible = []
        if self.obj.gender not in [MALE, FEMALE]:
            reasons_ineligible.append("gender invalid")
        if self.obj.age_in_years < 18:
            reasons_ineligible.append("age<18")
        if self.obj.hiv_pos == NO:
            reasons_ineligible.append("not HIV+")
        if self.obj.art_six_months == NO:
            reasons_ineligible.append("ART<6m")
        if self.obj.on_rx_stable == NO:
            reasons_ineligible.append("ART not stable")
        if self.obj.lives_nearby == NO:
            reasons_ineligible.append("Not living nearby")
        if get_meta_version() == PHASE_THREE and self.obj.staying_nearby_12 == NO:
            reasons_ineligible.append("Unable/Unwilling to stay nearby")
        elif self.obj.staying_nearby_6 == NO:
            reasons_ineligible.append("Unable/Unwilling to stay nearby")
        if self.obj.pregnant == YES:
            reasons_ineligible.append("Pregnant (unconfirmed)")
        eligible = NO if reasons_ineligible else YES
        self.obj.eligible_part_one = eligible
        self.obj.reasons_ineligible_part_one = "|".join(reasons_ineligible)
        if self.obj.eligible_part_one == YES or self.obj.eligible_part_two != TBD:
            self.obj.continue_part_two = YES

    def calculate_eligible_part_two(self):
        """Updates model instance fields `eligible_part_two`
        and `reasons_ineligible_part_two`.
        """
        self.obj.eligible_part_two = TBD
        self.obj.reasons_ineligible_part_two = None

        check_for_required_field_values(
            self.obj, get_part2_required_fields(), EligibilityPartTwoError
        )

        reasons_ineligible = []

        responses = {}
        for field in get_part2_required_fields():
            responses.update({field: getattr(self.obj, field)})
        for k, v in responses.items():
            if v == YES:
                reasons_ineligible.append(k.title().replace("_", " "))
        if not reasons_ineligible and self.obj.advised_to_fast == NO:
            reasons_ineligible.append("Not advised to fast")
        if not reasons_ineligible and not self.obj.appt_datetime:
            reasons_ineligible.append("Not scheduled for stage 2")
        eligible = NO if reasons_ineligible else YES
        self.obj.eligible_part_two = eligible
        self.obj.reasons_ineligible_part_two = "|".join(reasons_ineligible)

    def calculate_eligible_part_three(self):
        """Updates model instance fields `eligible_part_three`
        and `reasons_ineligible_part_three`.
        """
        self.obj.eligible_part_three = TBD
        self.obj.reasons_ineligible_part_three = None

        self.obj.converted_creatinine_value = convert_units(
            self.obj.creatinine_value,
            units_from=self.obj.creatinine_units,
            units_to=MICROMOLES_PER_LITER,
        )

        self.obj.converted_ifg_value = convert_units(
            self.obj.ifg_value,
            units_from=self.obj.ifg_units,
            units_to=MILLIMOLES_PER_LITER,
        )

        self.obj.converted_ogtt_value = convert_units(
            self.obj.ogtt_value,
            units_from=self.obj.ogtt_units,
            units_to=MILLIMOLES_PER_LITER,
        )

        self.obj.calculated_bmi_value = calculate_bmi(self.obj)

        if get_meta_version() == PHASE_TWO:
            a, b, c, d = calculate_inclusion_field_values_phase_two(self.obj)
            self.obj.inclusion_a = a
            self.obj.inclusion_b = b
            self.obj.inclusion_c = c
            self.obj.inclusion_d = d
            reasons_ineligible = []
            if any(
                [
                    self.obj.inclusion_a == TBD,
                    self.obj.inclusion_b == TBD,
                    self.obj.inclusion_c == TBD,
                    self.obj.inclusion_d == TBD,
                ]
            ):
                reasons_ineligible.append(BMI_IFT_OGTT_INCOMPLETE)
                self.obj.eligible_part_three = TBD
            if all(
                [
                    self.obj.inclusion_a == NO,
                    self.obj.inclusion_b == NO,
                    self.obj.inclusion_c == NO,
                    self.obj.inclusion_d == NO,
                ]
            ):
                reasons_ineligible.append(BMI_IFT_OGTT)
                self.obj.eligible_part_three = NO
            if not reasons_ineligible:
                self.obj.calculated_egfr_value = calculate_egfr(self.obj)
                if not self.obj.calculated_egfr_value:
                    reasons_ineligible.append(EGFR_NOT_CALCULATED)
                    self.obj.eligible_part_three = TBD
                elif self.obj.calculated_egfr_value < 45.0:
                    reasons_ineligible.append(EGFR_LT_45)
                    self.obj.eligible_part_three = NO

            if not reasons_ineligible:
                self.obj.eligible_part_three = YES
            elif (
                BMI_IFT_OGTT_INCOMPLETE not in reasons_ineligible
                and EGFR_NOT_CALCULATED not in reasons_ineligible
            ):
                self.obj.eligible_part_three = NO
            self.obj.reasons_ineligible_part_three = "|".join(reasons_ineligible)
        elif get_meta_version() == PHASE_THREE:
            a, b = calculate_inclusion_field_values_phase_three(self.obj)
            self.obj.inclusion_a = a
            self.obj.inclusion_b = b
            reasons_ineligible = []
            if any([self.obj.inclusion_a == TBD, self.obj.inclusion_b == TBD]):
                reasons_ineligible.append(IFT_OGTT_INCOMPLETE)
                self.obj.eligible_part_three = TBD
            if all([self.obj.inclusion_a == NO, self.obj.inclusion_b == NO]):
                reasons_ineligible.append(IFT_OGTT)
                self.obj.eligible_part_three = NO
            if self.obj.severe_htn == YES:
                reasons_ineligible.append(SEVERE_HTN)
            if not reasons_ineligible:
                self.obj.calculated_egfr_value = calculate_egfr(self.obj)
                if not self.obj.calculated_egfr_value:
                    reasons_ineligible.append(EGFR_NOT_CALCULATED)
                    self.obj.eligible_part_three = TBD
                elif self.obj.calculated_egfr_value < 45.0:
                    reasons_ineligible.append(EGFR_LT_45)
                    self.obj.eligible_part_three = NO
            if not reasons_ineligible:
                self.obj.eligible_part_three = YES
            elif (
                IFT_OGTT_INCOMPLETE not in reasons_ineligible
                and EGFR_NOT_CALCULATED not in reasons_ineligible
            ):
                self.obj.eligible_part_three = NO
            self.obj.reasons_ineligible_part_three = "|".join(reasons_ineligible)

    @property
    def eligibility_display_label(self):
        responses = [
            self.obj.eligible_part_one,
            self.obj.eligible_part_two,
            self.obj.eligible_part_three,
        ]
        if self.obj.eligible:
            display_label = "ELIGIBLE"
        elif TBD in responses and NO not in responses:
            if self.obj.reasons_ineligible == EGFR_NOT_CALCULATED:
                display_label = "PENDING (SCR/eGFR)"
            else:
                display_label = "PENDING"
        elif (
            self.obj.eligible_part_one == YES
            and self.obj.eligible_part_two == YES
            and BMI_IFT_OGTT_INCOMPLETE in self.obj.reasons_ineligible
        ):
            display_label = "PENDING (BMI/IFT/OGTT)"
        elif (
            self.obj.eligible_part_one == YES
            and self.obj.eligible_part_two == YES
            and self.obj.reasons_ineligible == EGFR_NOT_CALCULATED
        ):
            display_label = "PENDING (SCR/eGFR)"
        else:
            display_label = "not eligible"
        return display_label

    @property
    def eligibility_status(self):
        status_str = (
            f"P1: {self.obj.eligible_part_one.upper()}<BR>"
            f"P2: {self.obj.eligible_part_two.upper()}<BR>"
            f"P3: {self.obj.eligible_part_three.upper()}<BR>"
        )
        display_label = self.eligibility_display_label

        if "PENDING" in display_label:
            display_label = f'<font color="orange"><B>{display_label}</B></font>'

        return status_str + display_label
