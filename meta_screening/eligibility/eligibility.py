from edc_constants.constants import NO, TBD, YES
from edc_utils import get_utcnow

from meta_screening.constants import BMI_IFT_OGTT_INCOMPLETE, EGFR_NOT_CALCULATED


class SubjectScreeningEligibilityError(Exception):
    pass


class Eligibility:
    """
    Determines if a subject is eligible or not.

    Eligibility is assessed in three parts.

    Instantiated in the save() method of the screening proxy models.

    For example, for part one:

        def save(self, *args, **kwargs):
            eligibility = Eligibility(self)
            try:
                eligibility.assess_eligibility_for_part_one()
            except EligibilityPartOneError:
                pass
            eligibility.update_eligibility_fields()
            super().save(*args, **kwargs)

    """

    eligibility_values = [YES, NO, TBD]

    def __init__(self, obj):
        self.obj = obj

    def update_eligibility_fields(self):
        """Updates model instance fields `eligible`, `eligibility_datetime` and
        `reasons_ineligible`.
        """
        reasons_ineligible = []
        if self.obj.unsuitable_for_study == YES:
            self.obj.eligible = False
            reasons_ineligible.append("Subject unsuitable")
        else:
            self.obj.eligible = self.is_eligible
        if self.obj.eligible:
            self.obj.reasons_ineligible = None
        else:
            reasons_ineligible = self.get_reasons_if_ineligible(reasons_ineligible)
            if reasons_ineligible:
                self.obj.reasons_ineligible = "|".join(reasons_ineligible)
            else:
                self.obj.reasons_ineligible = None
        self.obj.eligibility_datetime = (
            self.obj.part_three_report_datetime or get_utcnow()
        )

    def get_reasons_if_ineligible(self, reasons_ineligible):
        if self.obj.reasons_ineligible_part_one:
            reasons_ineligible.append(self.obj.reasons_ineligible_part_one)
        if self.obj.reasons_ineligible_part_two:
            reasons_ineligible.append(self.obj.reasons_ineligible_part_two)
        if self.obj.reasons_ineligible_part_three:
            reasons_ineligible.append(self.obj.reasons_ineligible_part_three)
        return reasons_ineligible

    @property
    def is_eligible(self):
        """Returns True if eligible else False"""
        return True if self.eligible == YES else False

    @property
    def eligible(self):
        """Returns YES, NO or TBD.

        Can only be final if all three parts have been assessed.
        """
        eligible = NO
        p1_value = self.obj.eligible_part_one
        p2_value = self.obj.eligible_part_two
        p3_value = self.obj.eligible_part_three
        self.check_eligibility_values_or_raise(p1_value, p2_value, p3_value)
        for part in [p1_value, p2_value, p3_value]:
            if part not in self.eligibility_values:
                raise SubjectScreeningEligibilityError(
                    "Invalid value for `eligible`. "
                    f"Expected one of [{self.eligibility_values}]. Got `{part}`."
                )
        if p1_value == TBD or p2_value == TBD or p3_value == TBD:
            eligible = TBD
        if p1_value == YES and p2_value == YES and p3_value == YES:
            eligible = YES
        return eligible

    def check_eligibility_values_or_raise(self, p1_value, p2_value, p3_value):
        for part in [p1_value, p2_value, p3_value]:
            if part not in self.eligibility_values:
                raise SubjectScreeningEligibilityError(
                    "Invalid value for `eligible`. "
                    f"Expected one of [{self.eligibility_values}]. Got `{part}`."
                )

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
