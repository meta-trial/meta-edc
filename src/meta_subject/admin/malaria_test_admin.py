from django.contrib import admin
from edc_microscopy.modeladmin_mixins import MalariaTestModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import MalariaTestForm
from ..models import MalariaTest
from .modeladmin import CrfModelAdminMixin


@admin.register(MalariaTest, site=meta_subject_admin)
class MalariaTestAdmin(MalariaTestModelAdminMixin, CrfModelAdminMixin, SimpleHistoryAdmin):
    form = MalariaTestForm
