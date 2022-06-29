from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_identifier.model_mixins import TrackingModelMixin
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future, datetime_not_future
from edc_offstudy.constants import END_OF_STUDY_ACTION
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from meta_lists.models import OffstudyReasons

from ..choices import CLINICAL_WITHDRAWAL_REASONS, TOXICITY_WITHDRAWAL_REASONS

# TODO: confirm all appointments are either new, incomplete or done
# TODO: take off study meds but coninue followup (WITHDRAWAL)
# TODO: follow on new schedule, if permanently off drug (Single 36m visit)


class EndOfStudy(OffScheduleModelMixin, ActionModelMixin, TrackingModelMixin, BaseUuidModel):

    action_name = END_OF_STUDY_ACTION

    tracking_identifier_prefix = "ST"

    offschedule_datetime = models.DateTimeField(
        verbose_name="Date patient was terminated from the study",
        validators=[datetime_not_future],
        blank=False,
        null=True,
    )

    last_seen_date = models.DateField(
        verbose_name="Date patient was last seen",
        validators=[date_not_future],
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

    class Meta(OffScheduleModelMixin.Meta):
        verbose_name = "End of Study"
        verbose_name_plural = "End of Study"
