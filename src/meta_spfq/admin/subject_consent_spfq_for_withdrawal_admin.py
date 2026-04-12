from django.contrib import admin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_spfq_admin
from ..forms import SubjectConsentSpfqForWithdrawalForm
from ..models import SubjectConsentSpfqForWithdrawal
from .modeladmin_mixins import SpfqConsentModelAdminMixin


@admin.register(SubjectConsentSpfqForWithdrawal, site=meta_spfq_admin)
class SubjectConsentSpfqForWithdrawalAdmin(
    SpfqConsentModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentSpfqForWithdrawalForm
