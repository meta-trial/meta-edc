from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_identifier.model_mixins import TrackingModelMixin
from edc_model.models import BaseUuidModel
from edc_model.validators.date import datetime_not_future, date_not_future
from edc_visit_schedule.model_mixins import OffScheduleModelMixin
from meta_lists.models import OffstudyReasons

from ..constants import END_OF_STUDY_ACTION


class EndOfStudy(
    OffScheduleModelMixin, ActionModelMixin, TrackingModelMixin, BaseUuidModel
):

    action_name = END_OF_STUDY_ACTION

    tracking_identifier_prefix = "ST"

    offschedule_datetime = models.DateTimeField(
        verbose_name="Date patient was terminated from the study",
        validators=[datetime_not_future],
        blank=False,
        null=True,
    )

    offschedule_reason = models.ForeignKey(
        OffstudyReasons,
        verbose_name="Reason patient was terminated from the study",
        on_delete=models.PROTECT,
        null=True,
    )

    other_offschedule_reason = models.TextField(
        verbose_name="If OTHER, please specify", max_length=500, blank=True, null=True
    )

    death_date = models.DateField(
        verbose_name="Date of death, if applicable",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    transferred_consent = models.CharField(
        verbose_name=(
            "If transferred, has the patient provided consent to be followed-up?"
        ),
        choices=YES_NO_NA,
        max_length=15,
        default=NOT_APPLICABLE,
    )

    class Meta(OffScheduleModelMixin.Meta):
        verbose_name = "End of Study"
        verbose_name_plural = "End of Study"
