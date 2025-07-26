from edc_crf.modeladmin_mixins import CrfStatusModelAdminMixin
from edc_model_admin.dashboard import (
    ModelAdminCrfDashboardMixin,
    ModelAdminSubjectDashboardMixin,
)
from edc_model_admin.mixins import ModelAdminProtectPiiMixin
from edc_sites.admin import SiteModelAdminMixin


class ModelAdminMixin(ModelAdminSubjectDashboardMixin):
    pass


class CrfModelAdminMixin(
    ModelAdminProtectPiiMixin,
    SiteModelAdminMixin,
    CrfStatusModelAdminMixin,
    ModelAdminCrfDashboardMixin,
):
    pass
