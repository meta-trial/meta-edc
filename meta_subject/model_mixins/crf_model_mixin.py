from edc_crf.crf_model_mixin import CrfModelMixin as BaseCrfModelMixin
from edc_crf.crf_status_model_mixin import CrfStatusModelMixin
from edc_crf.crf_with_action_model_mixin import (
    CrfWithActionModelMixin as BaseCrfWithActionModelMixin,
)


class CrfModelMixin(CrfStatusModelMixin, BaseCrfModelMixin):
    class Meta(BaseCrfModelMixin.Meta):
        abstract = True


class CrfWithActionModelMixin(CrfStatusModelMixin, BaseCrfWithActionModelMixin):
    class Meta(BaseCrfModelMixin.Meta):
        abstract = True
