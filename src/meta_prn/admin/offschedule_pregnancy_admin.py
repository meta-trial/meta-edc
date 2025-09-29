from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django_audit_fields import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_action_item.modeladmin_mixins import ActionItemModelAdminMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import meta_prn_admin
from ..forms import OffSchedulePregnancyForm
from ..models import EndOfStudy, OffSchedulePregnancy


@admin.register(OffSchedulePregnancy, site=meta_prn_admin)
class OffSchedulePregnancyAdmin(
    SiteModelAdminMixin,
    ActionItemModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    instructions = None

    additional_instructions = mark_safe(  # noqa: S308
        render_to_string(
            "meta_prn/offschedule/additional_instructions.html",
            context=dict(verbose_name=EndOfStudy._meta.verbose_name),
        )
    )

    form = OffSchedulePregnancyForm

    fieldsets = (
        (None, {"fields": ("subject_identifier", "offschedule_datetime")}),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    def get_list_display(self, request) -> tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = ("subject_identifier", "dashboard", "offschedule_datetime")
        return custom_fields + tuple(f for f in list_display if f not in custom_fields)

    def get_list_filter(self, request) -> tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = ("offschedule_datetime",)
        return custom_fields + tuple(f for f in list_filter if f not in custom_fields)

    # def get_readonly_fields(self, request, obj=None) -> Tuple[str, ...]:
    #     custom_fields = ("subject_identifier", "offschedule_datetime")
    #     return tuple(set(super().get_readonly_fields(request, obj=obj) +
    #     custom_fields))
