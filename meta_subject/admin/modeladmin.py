from edc_model_admin.dashboard import (
    ModelAdminCrfDashboardMixin,
    ModelAdminSubjectDashboardMixin,
)
from edc_model_admin.history import SimpleHistoryAdmin


class ModelAdminMixin(ModelAdminSubjectDashboardMixin):
    pass


class CrfModelAdminMixin(ModelAdminCrfDashboardMixin):

    pass


class CrfModelAdmin(ModelAdminCrfDashboardMixin, SimpleHistoryAdmin):

    pass
