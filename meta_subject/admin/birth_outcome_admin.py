from typing import Tuple

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django_audit_fields.admin import audit_fieldset_tuple
from edc_data_manager.modeladmin_mixins import DataManagerModelAdminMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_registration.models import RegisteredSubject

from ..admin_site import meta_subject_admin
from ..forms import BirthOutcomesForm
from ..models import BirthOutcomes


@admin.register(BirthOutcomes, site=meta_subject_admin)
class BirthOutcomesAdmin(
    DataManagerModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):

    form = BirthOutcomesForm

    fieldsets = (
        (None, {"fields": ("delivery", "report_datetime")}),
        (
            "Birth Outcome",
            {
                "fields": (
                    "birth_order",
                    "birth_outcome",
                    "birth_weight",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "delivery_report",
        "dashboard",
        "birth_order",
        "birth_outcome",
    )

    radio_fields = {
        "birth_outcome": admin.VERTICAL,
    }

    def get_list_filter(self, request) -> Tuple[str, ...]:
        fields = super().get_list_filter(request)
        custom_fields = (
            "birth_order",
            "birth_outcome",
        )
        return custom_fields + fields

    def get_search_fields(self, request) -> Tuple[str, ...]:
        fields = super().get_search_fields(request)
        custom_fields = (
            "delivery__action_identifier__subject_visit__subject_identifier",
            "delivery__action_identifier",
            "delivery__tracking_identifier",
        )
        return tuple(set(fields + custom_fields))

    @admin.display
    def delivery_report(self, obj=None, label=None):
        url = reverse("meta_prn_admin:meta_prn_delivery_changelist")
        url = f"{url}?q={obj.subject_identifier}"
        context = dict(title="Delivery", url=url, label="Delivery")
        return render_to_string("dashboard_button.html", context=context)

    def get_subject_dashboard_url_kwargs(self, obj):
        return dict(subject_identifier=obj.subject_identifier)

    def view_on_site(self, obj):
        try:
            RegisteredSubject.objects.get(subject_identifier=obj.subject_identifier)
        except ObjectDoesNotExist:
            url = reverse(self.get_subject_listboard_url_name())
        else:
            try:
                url = reverse(
                    self.get_subject_dashboard_url_name(),
                    kwargs=self.get_subject_dashboard_url_kwargs(obj),
                )
            except NoReverseMatch as e:
                if callable(super().view_on_site):
                    url = super().view_on_site(obj)
                else:
                    raise NoReverseMatch(
                        f"{e}. See subject_dashboard_url_name for {repr(self)}."
                    )
        return url
