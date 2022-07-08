from django.contrib import admin
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_transfer.modeladmin_mixins import SubjectTransferModelAdminMixin

from ..admin_site import meta_prn_admin
from ..forms import SubjectTransferForm
from ..models import SubjectTransfer


@admin.register(SubjectTransfer, site=meta_prn_admin)
class SubjectTransferAdmin(
    SubjectTransferModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = SubjectTransferForm
