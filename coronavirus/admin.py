from django.contrib import admin
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from sarscov2.admin import CoronaKapModelAdminMixin

from .admin_site import coronavirus_admin
from .forms import CoronaKapForm
from .models import CoronaKap


@admin.register(CoronaKap, site=coronavirus_admin)
class CoronaKapAdmin(
    ModelAdminSubjectDashboardMixin,
    CoronaKapModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = CoronaKapForm
