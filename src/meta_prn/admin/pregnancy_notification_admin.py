from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_action_item.modeladmin_mixins import ActionItemModelAdminMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from meta_subject.models import UrinePregnancy

from ..admin_site import meta_prn_admin
from ..forms import PregnancyNotificationForm
from ..models import PregnancyNotification


@admin.register(PregnancyNotification, site=meta_prn_admin)
class PregnancyNotificationAdmin(
    SiteModelAdminMixin,
    ActionItemModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = PregnancyNotificationForm

    additional_instructions = (
        "Important: A positive Urine βhCG must be entered before this form "
        f"may be completed (See `{UrinePregnancy._meta.verbose_name}`)."
    )

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        (
            "Pregnancy",
            {"fields": ("bhcg_confirmed", "unconfirmed_details", "bhcg_date")},
        ),
        (
            "Delivery",
            {"fields": ("edd",)},
        ),
        (
            "Followup",
            {"fields": ("may_contact",)},
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "bhcg_confirmed": admin.VERTICAL,
        "may_contact": admin.VERTICAL,
    }

    def get_list_display(self, request) -> tuple[str, ...]:
        list_display = super().get_list_display(request)
        custom_fields = (
            "subject_identifier",
            "dashboard",
            "edd",
            "contact_agreed",
        )
        return custom_fields + tuple(f for f in list_display if f not in custom_fields)

    def get_list_filter(self, request) -> tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = ("edd", "may_contact")
        return custom_fields + tuple(f for f in list_filter if f not in custom_fields)

    @admin.display(description="May contact?", ordering="may_contact")
    def contact_agreed(self, obj):
        return obj.may_contact
