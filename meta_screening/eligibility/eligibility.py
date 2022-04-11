from django.db import models
from edc_constants.constants import NO, TBD, YES
from edc_utils import get_utcnow

from meta_screening.constants import BMI_FBG_OGTT_INCOMPLETE, EGFR_NOT_CALCULATED

from .eligibility_part_one import EligibilityPartOne
from .eligibility_part_three import EligibilityPartThreePhaseThree
from .eligibility_part_two import EligibilityPartTwo


class SubjectScreeningEligibilityError(Exception):
    pass


class MetaEligibility:
    """A wrapper class for three eligibility classes.

    Determines if a subject is eligible or not.

    Eligibility is assessed in three parts.

    Instantiated in the save() method of the screening proxy models.

    # For example, for part one:
    #
    #     def save(self, *args, **kwargs):
    #         eligibility = Eligibility(self)
    #         try:
    #             eligibility.assess_eligibility_for_part_one()
    #         except EligibilityPartOneError:
    #             pass
    #         eligibility.update_eligibility_fields()
    #         super().save(*args, **kwargs)

    """

    eligibility_values = [YES, NO, TBD]
    default_options = dict(
        eligible_value_default=TBD,
        eligible_values_list=[YES, NO, TBD],
        is_eligible_value=YES,
    )

    def __init__(
        self,
        model_obj: models.Model = None,
        defaults: dict = None,
        update_model=None,
    ):
        self.part_one = None
        self.part_two = None
        self.part_three = None
        self.update_model = True if update_model is None else update_model
        self.eligible = NO
        self.reasons_ineligible = {}
        self.model_obj = model_obj
        self.default_options = defaults or self.default_options
        self.assess_eligibility_for_all_parts()
        if self.update_model:
            self.update_model_final()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def assess_eligibility_for_all_parts(self):
        eligibility_part_one_cls = EligibilityPartOne
        eligibility_part_two_cls = EligibilityPartTwo
        eligibility_part_three_cls = EligibilityPartThreePhaseThree
        self.part_one = eligibility_part_one_cls(
            model_obj=self.model_obj,
            update_model=self.update_model,
            **self.default_options,
        )
        self.reasons_ineligible.update(**self.part_one.reasons_ineligible)
        self.part_two = eligibility_part_two_cls(
            model_obj=self.model_obj,
            update_model=self.update_model,
            **self.default_options,
        )
        self.reasons_ineligible.update(**self.part_two.reasons_ineligible)
        self.part_three = eligibility_part_three_cls(
            model_obj=self.model_obj,
            update_model=self.update_model,
            **self.default_options,
        )
        self.reasons_ineligible.update(**self.part_three.reasons_ineligible)
        if self.model_obj.unsuitable_for_study == YES:
            self.reasons_ineligible.update(unsuitable_for_study="Subject unsuitable")
        self.check_eligibility_values_or_raise()
        if all(
            [
                self.part_one.eligible == YES,
                self.part_two.eligible == YES,
                self.part_three.eligible == YES,
            ]
        ):
            self.eligible = YES
        elif any(
            [
                self.part_one.eligible == NO,
                self.part_two.eligible == NO,
                self.part_three.eligible == NO,
            ]
        ):
            self.eligible = NO
        elif any(
            [
                self.part_one.eligible == TBD,
                self.part_two.eligible == TBD,
                self.part_three.eligible == TBD,
                EGFR_NOT_CALCULATED in self.reasons_ineligible,
                BMI_FBG_OGTT_INCOMPLETE in self.reasons_ineligible,
            ]
        ):
            self.eligible = TBD

    def update_model_final(self):
        self.model_obj.reasons_ineligible = "|".join(self.reasons_ineligible)
        self.model_obj.eligible = self.is_eligible
        if self.is_eligible:
            self.model_obj.eligibility_datetime = (
                self.model_obj.part_three_report_datetime or get_utcnow()
            )
        else:
            self.model_obj.eligibility_datetime = None

    @property
    def is_eligible(self) -> bool:
        """Returns True if eligible else False"""
        return True if self.eligible == YES else False

    def check_eligibility_values_or_raise(self):
        for response in [
            self.part_one.eligible,
            self.part_two.eligible,
            self.part_three.eligible,
        ]:
            if response not in self.eligibility_values:
                raise SubjectScreeningEligibilityError(
                    "Invalid value for `eligible`. "
                    f"Expected one of [{self.eligibility_values}]. Got `{response}`."
                )

    @property
    def display_label(self):
        if self.eligible == YES:
            display_label = "ELIGIBLE"
        elif self.eligible == TBD:
            display_label = "PENDING"
            if EGFR_NOT_CALCULATED in self.reasons_ineligible:
                display_label = "PENDING (SCR/eGFR)"
            elif BMI_FBG_OGTT_INCOMPLETE in self.reasons_ineligible:
                display_label = "PENDING (BMI/IFT/OGTT)"
        else:
            display_label = "not eligible"
        return display_label

    @property
    def eligibility_status(self):
        status_str = (
            f"P1: {self.part_one.eligible.upper()}<BR>"
            f"P2: {self.part_two.eligible.upper()}<BR>"
            f"P3: {self.part_three.eligible.upper()}<BR>"
        )
        display_label = self.display_label
        if "PENDING" in display_label:
            display_label = f'<font color="orange"><B>{display_label}</B></font>'
        return status_str + display_label
