from django.contrib import admin
from edc_consent.modeladmin_mixins import ModelAdminConsentMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_consent_admin
from ..forms import SubjectConsentV1Form
from ..models import SubjectConsentV1
from .modeladmin_mixins import SubjectConsentModelAdminMixin


@admin.register(SubjectConsentV1, site=meta_consent_admin)
class SubjectConsentV1Admin(
    SubjectConsentModelAdminMixin,
    ModelAdminConsentMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentV1Form
