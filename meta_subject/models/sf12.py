from django.db import models
from django.utils.safestring import mark_safe
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
        verbose_name=mark_safe(
            "<b>Moderate activities</b> such as moving a table, "
            "pushing a vacuum cleaner, bowling, or playing golf:"
        ),
        max_length=20,
        choices=HEALTH_LIMITED_CHOICES,
    )

    climbing_stairs_now_limited = models.CharField(
        verbose_name=mark_safe("Climbing <b>several</b> flights of stairs:"),
        max_length=20,
        choices=HEALTH_LIMITED_CHOICES,
    )

    accomplished_less_physical_health = models.CharField(
        verbose_name=mark_safe("<b>Accomplished less</b> than you would like:"),
        max_length=15,
        choices=YES_NO,
    )

    work_limited_physical_health = models.CharField(
        verbose_name=mark_safe(
            "Were limited in the <b>kind</b> of work or other activities:"
        ),
        max_length=15,
        choices=YES_NO,
    )

    accomplished_less_emotional = models.CharField(
        verbose_name=mark_safe("<b>Accomplished less</b> than you would like:"),
        max_length=15,
        choices=YES_NO,
    )

    work_less_carefully_emotional = models.CharField(
        verbose_name=mark_safe(
            "Did work or activities <b>less carefully than usual</b>:"
        ),
        max_length=15,
        choices=YES_NO,
    )

    pain_interfere_work = models.CharField(
        verbose_name=mark_safe(
            "During the <u>past 4 weeks</u>, how much <u>did pain interfere</u> "
            "with your normal work (including work outside the home and housework)?"
        ),
        max_length=15,
        choices=WORK_PAIN_INTERFERENCE_CHOICES,
    )

    felt_calm_peaceful = models.CharField(
        verbose_name="Have you felt calm & peaceful?",
        max_length=25,
        choices=FEELING_DURATION_CHOICES,
    )

    felt_lot_energy = models.CharField(
        verbose_name="Did you have a lot of energy?",
        max_length=25,
        choices=FEELING_DURATION_CHOICES,
    )

    felt_down = models.CharField(
        verbose_name="Have you felt down-hearted and blue?",
        max_length=25,
        choices=FEELING_DURATION_CHOICES,
    )

    social_activities_interfered = models.CharField(
        verbose_name=mark_safe(
            "During the <u>past 4 weeks</u>, how much of the time has your physical "
            "health or emotional problems interfered with your social "
            "activities (like visiting friends, relatives, etc.)?"
        ),
        max_length=25,
        choices=INTERFERENCE_DURATION_CHOICES,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "SF-12 Health Survey"
        verbose_name_plural = "SF-12 Health Survey"
