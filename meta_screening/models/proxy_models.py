from edc_constants.constants import NO, TBD, YES

from meta_edc.meta_version import PHASE_THREE, get_meta_version

from ..eligibility import (
    EligibilityPartOne,
    EligibilityPartThreePhaseThree,
    EligibilityPartThreePhaseTwo,
    EligibilityPartTwo,
)
from .subject_screening import SubjectScreening

options = dict(
    eligible_value_default=TBD,
    eligible_values_list=[YES, NO, TBD],
    is_eligible_value=YES,
)


class ScreeningPartOne(SubjectScreening):
    def save(self, *args, **kwargs):
        # EligibilityPartOne(model_obj=self, **options)
        # self.eligible_part_one = eligibility.eligible
        # self.reasons_ineligible_part_one = eligibility.reasons_ineligible_as_str or None
        if self.eligible_part_one == YES:
            self.continue_part_two = YES
        else:
            self.continue_part_two = NO
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "Subject Screening: Part One"
        verbose_name_plural = "Subject Screening: Part One"


class ScreeningPartTwo(SubjectScreening):
    # def save(self, *args, **kwargs):
    #     EligibilityPartTwo(model_obj=self, **options)
    #     # self.eligible_part_two = eligibility.eligible
    #     # self.reasons_ineligible_part_two = eligibility.reasons_ineligible_as_str
    #     super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "Subject Screening: Part Two"
        verbose_name_plural = "Subject Screening: Part Two"


class ScreeningPartThree(SubjectScreening):
    # def save(self, *args, **kwargs):
    #     if get_meta_version() == PHASE_THREE:
    #         EligibilityPartThreePhaseThree(model_obj=self, **options)
    #     else:
    #         EligibilityPartThreePhaseTwo(model_obj=self, **options)
    #     super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "Subject Screening: Part Three"
        verbose_name_plural = "Subject Screening: Part Three"
