from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import AeTmgModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import meta_ae_admin
from ..forms import AeTmgForm
from ..models import AeTmg


@admin.register(AeTmg, site=meta_ae_admin)
class AeTmgAdmin(SiteModelAdminMixin, AeTmgModelAdminMixin, SimpleHistoryAdmin):
    form = AeTmgForm
