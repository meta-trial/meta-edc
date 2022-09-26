from edc_crf.model_mixins import CrfStatusModelMixin
from edc_crf.model_mixins import CrfWithActionModelMixin as BaseCrfWithActionModelMixin


class CrfWithActionModelMixin(CrfStatusModelMixin, BaseCrfWithActionModelMixin):
    class Meta(BaseCrfWithActionModelMixin.Meta):
        abstract = True
