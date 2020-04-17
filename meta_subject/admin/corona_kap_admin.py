from django.contrib import admin
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin
from sarscov2.admin import CoronaKapModelAdminMixin, fieldsets

from ..admin_site import meta_subject_admin
from ..forms import CoronaKapForm
from ..models import CoronaKap
from .modeladmin import CrfModelAdminMixin


@admin.register(CoronaKap, site=meta_subject_admin)
class CoronaKapAdmin(
    CrfModelAdminMixin,
    CoronaKapModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = CoronaKapForm
