from arrow import arrow
from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_identifier.model_mixins import TrackingModelMixin
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future, datetime_not_future
from edc_offstudy.constants import END_OF_STUDY_ACTION
from edc_protocol.validators import (
    date_not_before_study_start,
    datetime_not_before_study_start,
)
from edc_visit_schedule.model_mixins.schedule_model_mixin import ScheduleModelMixin

from meta_lists.models import OffstudyReasons

from ..choices import CLINICAL_WITHDRAWAL_REASONS, TOXICITY_WITHDRAWAL_REASONS

# TODO: confirm all appointments are either new, incomplete or done
# TODO: take off study meds but coninue followup (WITHDRAWAL)
# TODO: follow on new schedule, if permanently off drug (Single 36m visit)


class OffStudyModelMixin(models.Model):

    offstudy_datetime = models.DateTimeField(
        verbose_name="Date patient was terminated from the study",
        validators=[datetime_not_future],
        blank=False,
        null=True,
    )

    def save(self, *args, **kwargs):
        try:
            self.offstudy_datetime.date()
        except AttributeError:
            dt = self.offstudy_datetime.date()
            date_not_before_study_start(dt)
            date_not_future(dt)
        else:
            datetime_not_before_study_start(self.offstudy_datetime)
            datetime_not_future(self.offstudy_datetime)
        self.report_datetime = self.offstudy_datetime
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class EndOfStudy(
    OffStudyModelMixin, ScheduleModelMixin, ActionModelMixin, TrackingModelMixin, BaseUuidModel
):

    action_name = END_OF_STUDY_ACTION

    tracking_identifier_prefix = "ST"

    last_seen_date = models.DateField(
        verbose_name="Date patient was last seen",
        validators=[date_not_future],
        blank=False,
        null=True,
    )

    offstudy_reason = models.ForeignKey(
        OffstudyReasons,
        verbose_name="Reason patient was terminated from the study",
        on_delete=models.PROTECT,
        null=True,
    )

    other_offstudy_reason = models.TextField(
        verbose_name="If OTHER, please specify", max_length=500, blank=True, null=True
    )

    death_date = models.DateField(
        verbose_name="Date of death, if applicable",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    # PHASE THREE
    clinical_withdrawal_reason = models.CharField(
        verbose_name="If withdrawn for `clinical` reasons, please specify ...",
        max_length=25,
        choices=CLINICAL_WITHDRAWAL_REASONS,
        blank=True,
        null=True,
    )

    # PHASE THREE
    clinical_withdrawal_reason_other = models.TextField(
        verbose_name="If other `clinical` reason, please specify ...",
        max_length=500,
        blank=True,
        null=True,
    )

    # PHASE THREE
    toxicity_withdrawal_reason = models.CharField(
        verbose_name="If withdrawn for a `toxicity`, please specify ...",
        max_length=25,
        choices=TOXICITY_WITHDRAWAL_REASONS,
        blank=True,
        null=True,
    )

    # PHASE THREE
    toxicity_withdrawal_reason_other = models.TextField(
        verbose_name="If other `toxicity`, please specify ...",
        max_length=500,
        blank=True,
        null=True,
    )

    # TODO: 6m off drug and duration ?? See SOP
    ltfu_date = models.DateField(
        verbose_name="Date lost to followup, if applicable",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    transferred_consent = models.CharField(
        verbose_name="If transferred, has the patient provided consent to be followed-up?",
        choices=YES_NO_NA,
        max_length=15,
        default=NOT_APPLICABLE,
    )

    comment = models.TextField(
        verbose_name="Please provide further details if possible",
        max_length=500,
        blank=True,
        null=True,
    )

    class Meta(OffStudyModelMixin.Meta):
        verbose_name = "End of Study"
        verbose_name_plural = "End of Study"
