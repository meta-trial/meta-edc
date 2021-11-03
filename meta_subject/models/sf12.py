from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin

# TODO: Move to constants
ALL_OF_THE_TIME = "all_of_the_time"
MOST_OF_THE_TIME = "most_of_the_time"
GOOD_BIT_OF_THE_TIME = "good_bit_of_the_time"
SOME_OF_THE_TIME = "some_of_the_time"
LITTLE_OF_THE_TIME = "little_of_the_time"
NONE_OF_THE_TIME = "none_of_the_time"


# TODO: Move to choices
DESCRIBE_HEALTH_CHOICES = (
    ("excellent", "Excellent"),
    ("very_good", "Very good"),
    ("good", "Good"),
    ("fair", "Fair"),
    ("poor", "Poor"),
)

HEALTH_LIMITED_CHOICES = (
    ("limited_a_lot", "YES, limited a lot"),
    ("limited_a_little", "YES, limited a little"),
    ("not_limited_at_all", "NO, not at all limited"),
)

WORK_PAIN_INTERFERENCE_CHOICES = (
    ("not_at_all", "Not at all"),
    ("a_little_bit", "A little bit"),
    ("moderately", "Moderately"),
    ("quite_a-bit", "Quite a bit"),
    ("extremely", "Extremely"),
)

FEELING_DURATION_CHOICES = (
    (ALL_OF_THE_TIME, "All of the time"),
    (MOST_OF_THE_TIME, "Most of the time"),
    (GOOD_BIT_OF_THE_TIME, " A good bit of the time"),
    (SOME_OF_THE_TIME, "Some of the time"),
    (LITTLE_OF_THE_TIME, "A little of the time"),
    (NONE_OF_THE_TIME, "None of the time"),
)

INTERFERENCE_DURATION_CHOICES = (
    (ALL_OF_THE_TIME, "All of the time"),
    (MOST_OF_THE_TIME, "Most of the time"),
    (SOME_OF_THE_TIME, "Some of the time"),
    (LITTLE_OF_THE_TIME, "A little of the time"),
    (NONE_OF_THE_TIME, "None of the time"),
)


class Sf12(CrfModelMixin, edc_models.BaseUuidModel):
    # TODO: Refactor to edc-qol

    general_health = models.CharField(
        verbose_name="In general, would you say your health is:",
        max_length=15,
        choices=DESCRIBE_HEALTH_CHOICES,
    )

    moderate_activities_now_limited = models.CharField(
        verbose_name=(
            "During a typical day, does your health now limit you in: "
            "moderate activities such as moving a table, pushing a vacuum cleaner, "
            "bowling, or playing golf? If so, how much?"
        ),
        max_length=20,
        choices=HEALTH_LIMITED_CHOICES,
    )

    climbing_stairs_now_limited = models.CharField(
        verbose_name=(
            "During a typical day, does your health now limit you in: "
            "climbing several flights of stairs? If so, how much?"
        ),
        max_length=20,
        choices=HEALTH_LIMITED_CHOICES,
    )

    accomplished_less_physical_health = models.CharField(
        # TODO: verbose_name="",
        max_length=15,
        choices=YES_NO,
    )

    work_limited_physical_health = models.CharField(
        # TODO: verbose_name="",
        max_length=15,
        choices=YES_NO,
    )

    accomplished_less_emotional = models.CharField(
        # TODO: verbose_name="",
        max_length=15,
        choices=YES_NO,
    )

    work_less_carefully_emotional = models.CharField(
        # TODO: verbose_name="",
        max_length=15,
        choices=YES_NO,
    )

    pain_interfere_work = models.CharField(
        # TODO: verbose_name="",
        max_length=15,
        choices=WORK_PAIN_INTERFERENCE_CHOICES,
    )

    felt_calm_peaceful = models.CharField(
        # TODO: verbose_name="",
        max_length=25,
        choices=FEELING_DURATION_CHOICES,
    )

    felt_lot_energy = models.CharField(
        # TODO: verbose_name="",
        max_length=25,
        choices=FEELING_DURATION_CHOICES,
    )

    felt_down = models.CharField(
        # TODO: verbose_name="",
        max_length=25,
        choices=FEELING_DURATION_CHOICES,
    )

    social_activities_interfered = models.CharField(
        verboase_name=(
            "During the past 4 weeks, how much of the time has your physical "
            "health or emotional problems interfered with your social "
            "activities (like visiting friends, relatives, etc.)?"
        ),
        max_length=25,
        choices=INTERFERENCE_DURATION_CHOICES,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "SF-12 Health Survey"
        verbose_name_plural = "SF-12 Health Survey"
