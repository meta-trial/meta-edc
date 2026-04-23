from django.contrib import admin
from edc_data_manager.auth_objects import DATA_MANAGER_ROLE
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_spfq_admin
from ..forms import SubjectConsentSpfqForm
from ..models import SubjectConsentSpfq
from .modeladmin_mixins import SpfqConsentModelAdminMixin


@admin.register(SubjectConsentSpfq, site=meta_spfq_admin)
class SubjectConsentSpfqAdmin(
    SpfqConsentModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentSpfqForm

    def get_view_only_site_ids_for_user(self, request) -> list[int]:
        if request.user.userprofile.roles.filter(name=DATA_MANAGER_ROLE).exists():
            return [
                s.id for s in request.user.userprofile.sites.all() if s.id != request.site.id
            ]
        return super().get_view_only_site_ids_for_user(request)

    def user_may_view_other_sites(self, request) -> bool:  # noqa: ARG002
        return True
