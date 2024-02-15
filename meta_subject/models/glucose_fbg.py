from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import FASTING_CHOICES
from edc_constants.constants import EQ, FASTING
from edc_glucose.constants import GLUCOSE_HIGH_READING
from edc_lab.choices import RESULT_QUANTIFIER
from edc_lab_panel.model_mixin_factory import reportable_result_model_mixin_factory
from edc_model.models import BaseUuidModel
from edc_model.validators import datetime_not_future
from edc_reportable import (
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MILLIMOLES_PER_LITER_DISPLAY,
)

from ..model_mixins import CrfModelMixin


class GlucoseModelMixin(
    reportable_result_model_mixin_factory(
        utest_id="glucose",
        verbose_name="Glucose",
        units_choices=(
            (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
            (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER_DISPLAY),
        ),
        decimal_places=2,
        validators=[MinValueValidator(1.00), MaxValueValidator(GLUCOSE_HIGH_READING)],
        exclude_attrs_for_reportable=True,
    ),
    models.Model,
):
    fasting = models.CharField(
        verbose_name="Was this fasting or non-fasting?",
        max_length=25,
        choices=FASTING_CHOICES,
        null=True,
        blank=False,
    )

    glucose_quantifier = models.CharField(
        max_length=10,
        choices=RESULT_QUANTIFIER,
        default=EQ,
    )

    def get_summary_options(self) -> dict:
        opts = super().get_summary_options()  # noqa
        fasting = True if self.fasting == FASTING else False
        opts.update(fasting=fasting)
        return opts

    class Meta:
        abstract = True


class GlucoseFbg(
    CrfModelMixin,
    GlucoseModelMixin,
    BaseUuidModel,
):

    assay_datetime = models.DateTimeField(
        verbose_name="Result date and time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Glucose (FBG)"
        verbose_name_plural = "Glucose (FBG)"
