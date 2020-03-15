from django.db import models
from django.db.models.deletion import PROTECT
from edc_constants.choices import YES_NO
from edc_constants.constants import FASTING
from edc_crf.model_mixins import CrfNoManagerModelMixin
from edc_lab.choices import RESULT_QUANTIFIER
from edc_lab.constants import EQ
from edc_model.models import BaseUuidModel
from edc_model.validators import datetime_not_future
from edc_reportable import MILLIGRAMS_PER_DECILITER, MILLIMOLES_PER_LITER
from edc_reportable.choices import REPORTABLE
from edc_reportable.model_mixin import BloodResultsModelMixin

from ...choices import FASTING_CHOICES
from ...constants import BLOOD_RESULTS_GLU_ACTION
from ..subject_requisition import SubjectRequisition


class BloodResultsGlu(CrfNoManagerModelMixin, BloodResultsModelMixin, BaseUuidModel):

    action_name = BLOOD_RESULTS_GLU_ACTION

    tracking_identifier_prefix = "GL"

    is_poc = models.CharField(
        verbose_name="Was a point-of-care test used?",
        max_length=15,
        choices=YES_NO,
        null=True,
    )

    # blood glucose
    glucose_requisition = models.ForeignKey(
        SubjectRequisition,
        on_delete=PROTECT,
        related_name="bg",
        verbose_name="Requisition",
        null=True,
        blank=True,
        help_text=(
            "Start typing the requisition identifier or select one from this visit"
        ),
    )

    glucose_assay_datetime = models.DateTimeField(
        verbose_name="Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    fasting = models.CharField(
        verbose_name="Was this fasting or non-fasting?",
        max_length=25,
        choices=FASTING_CHOICES,
        null=True,
        blank=True,
    )

    glucose = models.DecimalField(
        verbose_name="Blood Glucose",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )

    glucose_quantifier = models.CharField(
        max_length=10, choices=RESULT_QUANTIFIER, default=EQ,
    )

    glucose_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=(
            (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
            (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER),
        ),
        null=True,
        blank=True,
    )

    glucose_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    glucose_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    def get_summary_options(self):
        opts = super().get_summary_options()
        fasting = True if self.fasting == FASTING else False
        opts.update(fasting=fasting)
        return opts

    class Meta(CrfNoManagerModelMixin.Meta):
        verbose_name = "Blood Result: Glucose"
        verbose_name_plural = "Blood Results: Glucose"
