from edc_model.models import BaseUuidModel
from edc_adverse_event.model_mixins import DeathReportTmgModelMixin


class DeathReportTmg(DeathReportTmgModelMixin, BaseUuidModel):
    class Meta(DeathReportTmgModelMixin.Meta):
        pass
