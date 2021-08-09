from meta_edc.meta_version import PHASE_THREE, get_meta_version

from ..eligibility import (
    EligibilityPartOne,
    EligibilityPartThreePhaseThree,
    EligibilityPartThreePhaseTwo,
    EligibilityPartTwo,
    RequiredFieldValueMissing,
)
from .subject_screening import SubjectScreening


class ScreeningPartOne(SubjectScreening):
    def save(self, *args, **kwargs):
        eligibility = EligibilityPartOne(self)
        try:
            eligibility.assess_eligibility()
        except RequiredFieldValueMissing:
            pass
        eligibility.update_eligibility_fields()
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "Subject Screening: Part One"
        verbose_name_plural = "Subject Screening: Part One"


class ScreeningPartTwo(SubjectScreening):
    def save(self, *args, **kwargs):
        eligibility = EligibilityPartTwo(self)
        try:
            eligibility.assess_eligibility()
        except RequiredFieldValueMissing:
            pass
        eligibility.update_eligibility_fields()
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "Subject Screening: Part Two"
        verbose_name_plural = "Subject Screening: Part Two"


class ScreeningPartThree(SubjectScreening):
    def save(self, *args, **kwargs):
        if get_meta_version() == PHASE_THREE:
            eligibility = EligibilityPartThreePhaseThree(self)
        else:
            eligibility = EligibilityPartThreePhaseTwo(self)
        eligibility.assess_eligibility()
        eligibility.update_eligibility_fields()
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "Subject Screening: Part Three"
        verbose_name_plural = "Subject Screening: Part Three"
