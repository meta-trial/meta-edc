from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import HospitalizationModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import meta_ae_admin
from ..forms import HospitalizationForm
from ..models import Hospitalization


@admin.register(Hospitalization, site=meta_ae_admin)
class HospitalizationAdmin(
    SiteModelAdminMixin, HospitalizationModelAdminMixin, SimpleHistoryAdmin
):
    form = HospitalizationForm
