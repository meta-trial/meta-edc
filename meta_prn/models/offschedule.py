from edc_action_item.models import ActionModelMixin
from edc_model.models import BaseUuidModel
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from ..constants import (
    OFFSCHEDULE_ACTION,
    OFFSCHEDULE_POSTNATAL_ACTION,
    OFFSCHEDULE_PREGNANCY_ACTION,
)


class OffSchedule(ActionModelMixin, OffScheduleModelMixin, BaseUuidModel):

    action_name = OFFSCHEDULE_ACTION

    class Meta(OffScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Off-schedule"
        verbose_name_plural = "Off-schedule"


class OffSchedulePregnancy(ActionModelMixin, OffScheduleModelMixin, BaseUuidModel):

    action_name = OFFSCHEDULE_PREGNANCY_ACTION

    class Meta(OffScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Off-schedule: Pregnancy"
        verbose_name_plural = "Off-schedule: Pregnancy"


class OffSchedulePostnatal(ActionModelMixin, OffScheduleModelMixin, BaseUuidModel):

    action_name = OFFSCHEDULE_POSTNATAL_ACTION

    class Meta(OffScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Off-schedule: post-natal"
        verbose_name_plural = "Off-schedule: post-natal"
