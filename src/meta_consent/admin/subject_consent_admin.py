from django.contrib import admin
from edc_consent.modeladmin_mixins import ModelAdminConsentMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_consent_admin
from ..forms import SubjectConsentForm
from ..models import SubjectConsent
from .modeladmin_mixins import SubjectConsentModelAdminMixin


@admin.register(SubjectConsent, site=meta_consent_admin)
class SubjectConsentAdmin(
    SubjectConsentModelAdminMixin,
    ModelAdminConsentMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentForm
