from django.contrib import admin
from edc_action_item.modeladmin_mixins import ActionItemModelAdminMixin
from edc_egfr.admin import EgfrDropNotificationAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import EgfrDropNotificationForm
from ..models import EgfrDropNotification
from .modeladmin import CrfModelAdminMixin


@admin.register(EgfrDropNotification, site=meta_subject_admin)
class EgfrDropNotificationAdmin(
    EgfrDropNotificationAdminMixin,
    CrfModelAdminMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = EgfrDropNotificationForm
