from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import AeFollowupModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import meta_ae_admin
from ..forms import AeFollowupForm
from ..models import AeFollowup


@admin.register(AeFollowup, site=meta_ae_admin)
class AeFollowupAdmin(SiteModelAdminMixin, AeFollowupModelAdminMixin, SimpleHistoryAdmin):
    form = AeFollowupForm
