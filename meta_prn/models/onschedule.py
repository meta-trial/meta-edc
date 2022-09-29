from edc_model.models import BaseUuidModel
from edc_sites.models import SiteModelMixin
from edc_visit_schedule.model_mixins import OnScheduleModelMixin


class OnSchedule(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by subject_consent."""

    class Meta(OnScheduleModelMixin.Meta, BaseUuidModel.Meta):
        pass


class OnSchedulePregnancy(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    class Meta(OnScheduleModelMixin.Meta, BaseUuidModel.Meta):
        pass


class OnSchedulePostnatal(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    class Meta(OnScheduleModelMixin.Meta):
        pass
