from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import meta_prn_admin
from ..models import OnSchedulePregnancy


@admin.register(OnSchedulePregnancy, site=meta_prn_admin)
class OnSchedulePregnancyAdmin(
    SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):
    instructions = None

    fieldsets = (
        (None, {"fields": ("subject_identifier", "onschedule_datetime")}),
        audit_fieldset_tuple,
    )

    def get_list_display(self, request) -> tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = ("subject_identifier", "dashboard", "onschedule_datetime")
        return custom_fields + tuple(
            f for f in list_display if f not in (*custom_fields, "__str__")
        )

    def get_list_filter(self, request) -> tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = ("onschedule_datetime",)
        return (
            *custom_fields,
            *[f for f in list_filter if f not in custom_fields],
        )

    def get_readonly_fields(self, request, obj=None) -> tuple[str, ...]:  # noqa: ARG002
        return (
            "subject_identifier",
            "onschedule_datetime",
        )

    def get_search_fields(self, request) -> tuple[str, ...]:
        fields = super().get_search_fields(request)
        return tuple({*fields, "subject_identifier"})
