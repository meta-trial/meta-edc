from django.contrib import admin
from edc_action_item import ActionItemModelAdminMixin
from edc_data_manager.modeladmin_mixins import DataManagerModelAdminMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_protocol_incident.modeladmin_mixins import ProtocolIncidentModelAdminMixin

from ..admin_site import meta_prn_admin
from ..forms import ProtocolIncidentForm
from ..models import ProtocolIncident


@admin.register(ProtocolIncident, site=meta_prn_admin)
class ProtocolIncidentAdmin(
    ProtocolIncidentModelAdminMixin,
    DataManagerModelAdminMixin,
    ActionItemModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):

    form = ProtocolIncidentForm
