from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from edc_constants.choices import YES_NO
from edc_crf.model_mixins import CrfNoManagerModelMixin
from edc_model.models import BaseUuidModel
from edc_model.validators import datetime_not_future
from edc_reportable import PERCENT
from edc_reportable.choices import REPORTABLE
from edc_reportable.model_mixin import BloodResultsModelMixin


from ...constants import BLOOD_RESULTS_HBA1C_ACTION
from ..subject_requisition import SubjectRequisition


class BloodResultsHba1c(CrfNoManagerModelMixin, BloodResultsModelMixin, BaseUuidModel):

    action_name = BLOOD_RESULTS_HBA1C_ACTION

    tracking_identifier_prefix = "HA"

    is_poc = models.CharField(
        verbose_name="Was a point-of-care test used?",
        max_length=15,
        choices=YES_NO,
        null=True,
    )

    # HbA1c
    hba1c_requisition = models.ForeignKey(
        SubjectRequisition,
        on_delete=PROTECT,
        related_name="hba1c",
        verbose_name="Requisition",
        null=True,
        blank=True,
        help_text=(
            "Start typing the requisition identifier or select one from this visit"
        ),
    )

    hba1c_assay_datetime = models.DateTimeField(
        verbose_name="Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    hba1c = models.DecimalField(
        verbose_name="HbA1c",
        max_digits=8,
        decimal_places=4,
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        null=True,
        blank=True,
    )

    hba1c_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((PERCENT, PERCENT),),
        null=True,
        blank=True,
    )

    hba1c_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    hba1c_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta(CrfNoManagerModelMixin.Meta):
        verbose_name = "Blood Result: HbA1c"
        verbose_name_plural = "Blood Results: HbA1c"
