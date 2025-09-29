from edc_action_item.models import ActionModelMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin
from edc_visit_schedule.constants import OFFSCHEDULE_ACTION
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from ..constants import (
    OFFSCHEDULE_DM_REFERRAL_ACTION,
    OFFSCHEDULE_POSTNATAL_ACTION,
    OFFSCHEDULE_PREGNANCY_ACTION,
)


class OffSchedule(SiteModelMixin, OffScheduleModelMixin, ActionModelMixin, BaseUuidModel):
    action_name = OFFSCHEDULE_ACTION
    offschedule_compare_dates_as_datetimes = False

    class Meta(OffScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Off-schedule"
        verbose_name_plural = "Off-schedule"


class OffSchedulePregnancy(
    SiteModelMixin, OffScheduleModelMixin, ActionModelMixin, BaseUuidModel
):
    action_name = OFFSCHEDULE_PREGNANCY_ACTION

    class Meta(OffScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Off-schedule: Pregnancy"
        verbose_name_plural = "Off-schedule: Pregnancy"


class OffSchedulePostnatal(
    SiteModelMixin, OffScheduleModelMixin, ActionModelMixin, BaseUuidModel
):
    action_name = OFFSCHEDULE_POSTNATAL_ACTION

    class Meta(OffScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Off-schedule: post-natal"
        verbose_name_plural = "Off-schedule: post-natal"


class OffScheduleDmReferral(
    SiteModelMixin, OffScheduleModelMixin, ActionModelMixin, BaseUuidModel
):
    action_name = OFFSCHEDULE_DM_REFERRAL_ACTION

    class Meta(OffScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Off-schedule: DM Referral"
        verbose_name_plural = "Off-schedule: DM Referral"
