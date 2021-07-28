from ..eligibility import Eligibility, EligibilityPartOneError, EligibilityPartTwoError
from .subject_screening import SubjectScreening


class ScreeningPartOne(SubjectScreening):
    def save(self, *args, **kwargs):
        eligibility = Eligibility(self)
        try:
            eligibility.calculate_eligible_part_one()
        except EligibilityPartOneError:
            pass
        eligibility.check_eligible_final()
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "Subject Screening: Part One"
        verbose_name_plural = "Subject Screening: Part One"


class ScreeningPartTwo(SubjectScreening):
    def save(self, *args, **kwargs):
        eligibility = Eligibility(self)
        try:
            eligibility.calculate_eligible_part_two()
        except EligibilityPartTwoError:
            pass
        eligibility.check_eligible_final()
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "Subject Screening: Part Two"
        verbose_name_plural = "Subject Screening: Part Two"


class ScreeningPartThree(SubjectScreening):
    def save(self, *args, **kwargs):
        eligibility = Eligibility(self)
        eligibility.calculate_eligible_part_three()
        eligibility.check_eligible_final()
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "Subject Screening: Part Three"
        verbose_name_plural = "Subject Screening: Part Three"
