from typing import Any

from clinicedc_constants import NO, TBD, YES
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from edc_utils import get_utcnow

from ..constants import EGFR_NOT_CALCULATED
from .eligibility_part_one import EligibilityPartOne
from .eligibility_part_three import EligibilityPartThreePhaseThree
from .eligibility_part_two import EligibilityPartTwo


class SubjectScreeningEligibilityError(Exception):
    pass


def get_eligible_as_word(  # noqa: PLR0913
    obj=None,
    eligible_part_one=None,
    eligible_part_two=None,
    eligible_part_three=None,
    unsuitable_for_study=None,
    reasons_ineligible=None,
):
    eligible = TBD
    reasons_ineligible = {} if reasons_ineligible is None else reasons_ineligible
    eligible_part_one = obj.eligible_part_one if obj else eligible_part_one
    eligible_part_two = obj.eligible_part_two if obj else eligible_part_two
    eligible_part_three = obj.eligible_part_three if obj else eligible_part_three
    unsuitable_for_study = obj.unsuitable_for_study if obj else unsuitable_for_study

    if unsuitable_for_study == YES:
        reasons_ineligible.update(unsuitable_for_study="Subject unsuitable")
        eligible = NO
    elif all(
        [
            eligible_part_one == YES,
            eligible_part_two == YES,
            eligible_part_three == YES,
        ]
    ):
        eligible = YES
    elif NO in [eligible_part_one, eligible_part_two, eligible_part_three]:
        eligible = NO
    elif TBD in [eligible_part_one, eligible_part_two, eligible_part_three]:
        eligible = TBD
    if eligible == YES and reasons_ineligible:
        raise SubjectScreeningEligibilityError(
            f"Expected reasons_ineligible to be None. Got {reasons_ineligible}."
        )
    return eligible, reasons_ineligible


def get_display_label(obj):
    eligible, _ = get_eligible_as_word(obj)
    if eligible == YES:
        display_label = "ELIGIBLE"
    elif eligible == TBD:
        display_label = "PENDING"
        if EGFR_NOT_CALCULATED in (obj.reasons_ineligible or {}):
            display_label = "PENDING (SCR/eGFR)"
        elif "fbg_ogtt_incomplete" in (obj.reasons_ineligible or {}):
            display_label = "PENDING (FBG/OGTT)"
    else:
        display_label = "not eligible"
    return display_label


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

    eligibility_values = (YES, NO, TBD)
    default_options = dict(  # noqa: RUF012
        eligible_value_default=TBD,
        eligible_values_list=[YES, NO, TBD],
        is_eligible_value=YES,
    )

    def __init__(
        self,
        model_obj: models.Model | None = None,
        defaults: dict | None = None,
        update_model=None,
    ):
        self.part_one = None
        self.part_two = None
        self.part_three = None
        self.update_model = True if update_model is None else update_model
        self.eligible = TBD
        self.reasons_ineligible = {}
        self.model_obj = model_obj
        self.default_options = defaults or self.default_options
        self.assess_eligibility_for_all_parts()
        if self.update_model:
            self.update_model_final()

    def __repr__(self: Any) -> str:
        return f"{self.__class__.__name__}()"

    def assess_eligibility_for_all_parts(self: Any):
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
        self.check_eligibility_values_or_raise()
        self.eligible, self.reasons_ineligible = get_eligible_as_word(
            eligible_part_one=self.part_one.eligible,
            eligible_part_two=self.part_two.eligible,
            eligible_part_three=self.part_three.eligible,
            reasons_ineligible=self.reasons_ineligible,
            unsuitable_for_study=self.model_obj.unsuitable_for_study,
        )

    def update_model_final(self: Any):
        self.model_obj.reasons_ineligible = "|".join(self.reasons_ineligible)
        self.model_obj.eligible = self.is_eligible
        if self.is_eligible:
            self.model_obj.eligibility_datetime = (
                self.model_obj.part_three_report_datetime or get_utcnow()
            )
        else:
            self.model_obj.eligibility_datetime = None

    @property
    def is_eligible(self: Any) -> bool:
        """Returns True if eligible else False"""
        return self.eligible == YES

    def check_eligibility_values_or_raise(self: Any):
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
    def display_label(self: Any):
        return get_display_label(obj=self.model_obj)

    def eligibility_status(self: Any, add_urls=None):
        if add_urls:
            url_p1 = reverse(
                "meta_screening_admin:meta_screening_screeningpartone_change",
                args=(self.part_one.model_obj.id,),
            )
            url_p2 = reverse(
                "meta_screening_admin:meta_screening_screeningparttwo_change",
                args=(self.part_two.model_obj.id,),
            )
            url_p3 = reverse(
                "meta_screening_admin:meta_screening_screeningpartthree_change",
                args=(self.part_three.model_obj.id,),
            )
            status_str = format_html(
                '<A href="{url_p1}">P1: {p1_eligible}</A>'
                '<BR><A href="{url_p2}">P2: {p2_eligible}</A>'
                '<BR><A href="{url_p3}">P3: {p3_eligible}</A><BR>',
                url_p1=url_p1,
                p1_eligible=self.part_one.eligible.upper(),
                url_p2=url_p2,
                p2_eligible=self.part_two.eligible.upper(),
                url_p3=url_p3,
                p3_eligible=self.part_three.eligible.upper(),
            )
        else:
            status_str = format_html(
                "P1: {p1_eligible}<BR>P2: {p2_eligible}<BR>P3: {p3_eligible}<BR>",
                p1_eligible=self.part_one.eligible.upper(),
                p2_eligible=self.part_two.eligible.upper(),
                p3_eligible=self.part_three.eligible.upper(),
            )
        display_label = self.display_label
        if "PENDING" in display_label:
            display_label = f'<font color="orange"><B>{display_label}</B></font>'
        return status_str + display_label
