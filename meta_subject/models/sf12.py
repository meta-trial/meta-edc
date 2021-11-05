from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from ..choices import (
    DESCRIBE_HEALTH_CHOICES,
    FEELING_DURATION_CHOICES,
    HEALTH_LIMITED_CHOICES,
    INTERFERENCE_DURATION_CHOICES,
    WORK_PAIN_INTERFERENCE_CHOICES,
)
from ..model_mixins import CrfModelMixin


class Sf12(CrfModelMixin, edc_models.BaseUuidModel):
    # TODO: Refactor to edc-qol

    general_health = models.CharField(
        verbose_name="In general, would you say your health is:",
        max_length=15,
        choices=DESCRIBE_HEALTH_CHOICES,
    )

    moderate_activities_now_limited = models.CharField(
        verbose_name=mark_safe(
            "<u>Moderate activities</u> such as moving a table, "
            "pushing a vacuum cleaner, bowling, or playing golf:"
        ),
        max_length=20,
        choices=HEALTH_LIMITED_CHOICES,
    )

    climbing_stairs_now_limited = models.CharField(
        verbose_name=mark_safe("Climbing <u>several</u> flights of stairs:"),
        max_length=20,
        choices=HEALTH_LIMITED_CHOICES,
    )

    accomplished_less_physical_health = models.CharField(
        verbose_name=mark_safe("<u>Accomplished less</u> than you would like:"),
        max_length=15,
        choices=YES_NO,
    )

    work_limited_physical_health = models.CharField(
        verbose_name=mark_safe(
            "Were limited in the <u>kind</u> of work or other activities:"
        ),
        max_length=15,
        choices=YES_NO,
    )

    accomplished_less_emotional = models.CharField(
        verbose_name=mark_safe("<u>Accomplished less</u> than you would like:"),
        max_length=15,
        choices=YES_NO,
    )

    work_less_carefully_emotional = models.CharField(
        verbose_name=mark_safe(
            "Did work or activities <u>less carefully than usual</u>:"
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
