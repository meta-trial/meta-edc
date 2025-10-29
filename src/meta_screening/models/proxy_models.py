from clinicedc_constants import NO, TBD, YES

from meta_consent.consents import consent_v1

from .subject_screening import SubjectScreening

options = dict(
    eligible_value_default=TBD,
    eligible_values_list=[YES, NO, TBD],
    is_eligible_value=YES,
)


class ScreeningPartOne(SubjectScreening):
    consent_definition = consent_v1

    def save(self, *args, **kwargs):
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
    consent_definition = consent_v1

    class Meta:
        proxy = True
        verbose_name = "Subject Screening: Part Two"
        verbose_name_plural = "Subject Screening: Part Two"


class ScreeningPartThree(SubjectScreening):
    consent_definition = consent_v1

    class Meta:
        proxy = True
        verbose_name = "Subject Screening: Part Three"
        verbose_name_plural = "Subject Screening: Part Three"
