from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_action_item.modeladmin_mixins import ActionItemModelAdminMixin
from edc_data_manager.auth_objects import DATA_MANAGER_ROLE
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.admin.list_filters import SitesForDataManagerListFilter

from meta_reports.models import EndpointsProxy

from ..admin_site import meta_prn_admin
from ..forms import DmReferralForm
from ..models import DmReferral


@admin.register(DmReferral, site=meta_prn_admin)
class DmReferralAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = DmReferralForm

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        ("Referral to Diabetes clinic", {"fields": ("referral_date",)}),
        (
            "Diabetes diagnosis",
            {
                "fields": ("referral_note",),
            },
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    list_display = (
        "subject_identifier",
        "dashboard",
        "report_datetime",
        "referral_date_as_col",
        "endpoint",
    )

    list_filter = ("report_datetime", "referral_date", SitesForDataManagerListFilter)

    @admin.display(description="Referral date", ordering="referral_date")
    def referral_date_as_col(self, obj=None):
        return obj.referral_date

    @admin.display(description="endpoint")
    def endpoint(self, obj=None):
        try:
            obj = EndpointsProxy.objects.get(subject_identifier=obj.subject_identifier)
        except ObjectDoesNotExist:
            pass
        else:
            url = reverse("meta_reports_admin:meta_reports_endpointsproxy_changelist")
            return format_html(
                '<A href="{url}?q={subject_identifier}">{referral_date}</A>',
                url=url,
                referral_date=obj.endpoint_label,
                subject_identifier=obj.subject_identifier,
            )
        return None

    def get_view_only_site_ids_for_user(self, request) -> list[int]:
        if request.user.userprofile.roles.filter(name=DATA_MANAGER_ROLE).exists():
            return [
                s.id for s in request.user.userprofile.sites.all() if s.id != request.site.id
            ]
        return super().get_view_only_site_ids_for_user(request)
