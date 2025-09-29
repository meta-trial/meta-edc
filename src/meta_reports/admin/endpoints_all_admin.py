from django.contrib import admin
from django.template.loader import render_to_string

from ..admin_site import meta_reports_admin
from ..models import EndpointsProxy
from .modeladmin_mixins import EndpointsModelAdminMixin


@admin.register(EndpointsProxy, site=meta_reports_admin)
class EndpointsAllAdmin(EndpointsModelAdminMixin, admin.ModelAdmin):
    def rendered_change_list_note(self):
        return render_to_string("meta_reports/endpoints_all_change_list_note.html")
