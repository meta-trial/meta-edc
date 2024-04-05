from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin
from edc_visit_schedule.model_mixins import OnScheduleModelMixin


class OnSchedule(OnScheduleModelMixin, SiteModelMixin, BaseUuidModel):
    """A model used by the system. Auto-completed by subject_consent."""

    class Meta(OnScheduleModelMixin.Meta, BaseUuidModel.Meta):
        pass


class OnSchedulePregnancy(OnScheduleModelMixin, SiteModelMixin, BaseUuidModel):
    class Meta(OnScheduleModelMixin.Meta, BaseUuidModel.Meta):
        pass


class OnSchedulePostnatal(OnScheduleModelMixin, SiteModelMixin, BaseUuidModel):
    class Meta(OnScheduleModelMixin.Meta):
        pass


class OnScheduleDmReferral(OnScheduleModelMixin, SiteModelMixin, BaseUuidModel):
    class Meta(OnScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "On-schedule: DM Referral"
        verbose_name_plural = "On-schedule: DM Referral"
