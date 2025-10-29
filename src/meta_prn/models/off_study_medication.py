from clinicedc_constants import NULL_STRING
from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_pharmacy.models import Medication
from edc_prn.models import SingletonPrnModelMixin
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow

from meta_pharmacy.constants import METFORMIN

from ..choices import WITHDRAWAL_STUDY_MEDICATION_REASONS
from ..constants import OFFSTUDY_MEDICATION_ACTION


class OffStudyMedication(
    UniqueSubjectIdentifierFieldMixin,
    SiteModelMixin,
    ActionModelMixin,
    SingletonPrnModelMixin,
    BaseUuidModel,
):
    action_name = OFFSTUDY_MEDICATION_ACTION

    offschedule_compare_dates_as_datetimes = False

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time", default=get_utcnow
    )

    medications = models.ManyToManyField(Medication, limit_choices_to={"name": METFORMIN})

    stop_date = models.DateField(
        verbose_name="Date decision to stop study medication",
    )

    last_dose_date = models.DateField(
        verbose_name="Date of last known dose",
    )

    reason = models.CharField(
        verbose_name="Reason for stopping study medication",
        max_length=25,
        choices=WITHDRAWAL_STUDY_MEDICATION_REASONS,
    )

    reason_other = models.TextField(
        verbose_name="If other, please specify ...",
        default=NULL_STRING,
        blank=True,
    )

    comment = models.TextField(
        verbose_name="Any additional comments",
        default=NULL_STRING,
        blank=True,
    )

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Withdrawal of Study Drug"
        verbose_name_plural = "Withdrawal of Study Drug"
