from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from meta_edc.meta_version import PHASE_THREE, get_meta_version

from ...admin_site import meta_prn_admin
from ...forms import EndOfStudyPhaseTwoForm
from ...models import EndOfStudy
from .model_admin_mixin import EndOfStudyAdminMixin


class EndOfStudyPhaseTwoAdmin(
    EndOfStudyAdminMixin,
    DataManagerModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):

    form = EndOfStudyPhaseTwoForm


if get_meta_version() != PHASE_THREE:
    meta_prn_admin.register(EndOfStudy, EndOfStudyPhaseTwoAdmin)
