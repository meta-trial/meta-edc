from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO
from edc_lab.choices import RESULT_QUANTIFIER
from edc_lab.constants import EQ
from edc_model.validators import hm_validator

from ..choices import GLUCOSE_UNITS


class FastingModelMixin(models.Model):
    fasted = models.CharField(
        verbose_name="Has the participant fasted?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    fasted_duration_str = models.CharField(
        verbose_name="How long have they fasted in hours and/or minutes?",
        max_length=8,
        validators=[hm_validator],
        null=True,
        blank=True,
        help_text="Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
    )

    fasted_duration_minutes = models.IntegerField(
        null=True, help_text="system calculated value"
    )

    class Meta:
        abstract = True


class FastingGlucoseModelMixin(models.Model):
    # IFG
    fasting_glucose = models.DecimalField(
        verbose_name=mark_safe("Fasting glucose <u>level</u>"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    fasting_glucose_quantifier = models.CharField(
        max_length=10, choices=RESULT_QUANTIFIER, default=EQ,
    )

    fasting_glucose_units = models.CharField(
        verbose_name="Units (fasting glucose)",
        max_length=15,
        choices=GLUCOSE_UNITS,
        blank=True,
        null=True,
    )

    fasting_glucose_datetime = models.DateTimeField(
        verbose_name=mark_safe("<u>Time</u> fasting glucose <u>level</u> measured"),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class OgttModelMixin(models.Model):
    ogtt_base_datetime = models.DateTimeField(
        verbose_name=mark_safe("<u>Time</u> oral glucose solution was given"),
        null=True,
        blank=True,
        help_text="(glucose solution given)",
    )

    ogtt_two_hr = models.DecimalField(
        verbose_name=mark_safe(
            "Blood glucose <u>level</u> 2-hours " "after oral glucose solution given"
        ),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    ogtt_two_hr_quantifier = models.CharField(
        max_length=10, choices=RESULT_QUANTIFIER, default=EQ,
    )

    ogtt_two_hr_units = models.CharField(
        verbose_name="Units (Blood glucose 2hrs after...)",
        max_length=15,
        choices=GLUCOSE_UNITS,
        blank=True,
        null=True,
    )

    ogtt_two_hr_datetime = models.DateTimeField(
        verbose_name=mark_safe(
            "<u>Time</u> blood glucose measured 2-hours "
            "after oral glucose solution given"
        ),
        blank=True,
        null=True,
        help_text="(2 hours after glucose solution given)",
    )

    class Meta:
        abstract = True
