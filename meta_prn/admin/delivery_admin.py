from copy import copy

from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from edc_action_item import action_fields, action_fieldset_tuple
from edc_data_manager.data_manager_modeladmin_mixin import DataManagerModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin, TabularInlineMixin, audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import meta_prn_admin
from ..forms import BirthOutcomesForm, DeliveryForm
from ..models import BirthOutcomes, Delivery


class BirthOutcomesInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = BirthOutcomes
    form = BirthOutcomesForm
    extra = 1
    fields = [
        "birth_order",
        "birth_outcome",
        "birth_weight",
    ]


@admin.register(Delivery, site=meta_prn_admin)
class DeliveryAdmin(
    DataManagerModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = DeliveryForm

    inlines = [BirthOutcomesInlineAdmin]

    fieldsets = (
        (None, {"fields": ("subject_identifier", "report_datetime")}),
        (
            "Source of information",
            {
                "fields": (
                    "informant_is_patient",
                    "informant_contact",
                    "informant_relation",
                    "informant_relation_other",
                )
            },
        ),
        (
            "Delivery",
            {
                "fields": (
                    "delivery_datetime",
                    "delivery_time_estimated",
                    "delivery_location",
                    "delivery_location_other",
                    "delivery_location_name",
                    "delivery_ga",
                    "gm_treated",
                    "maternal_outcome",
                )
            },
        ),
        (
            "Outcomes",
            {"fields": ("fetal_outcome_count",)},
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    list_display = (
        "subject_identifier",
        "birth_outcomes",
        "dashboard",
        "delivery_datetime",
        "maternal_outcome",
        "fetal_outcome_count",
    )

    list_filter = (
        "delivery_datetime",
        "gm_treated",
        "maternal_outcome",
    )

    radio_fields = {
        "informant_is_patient": admin.VERTICAL,
        "informant_relation": admin.VERTICAL,
        "delivery_time_estimated": admin.VERTICAL,
        "delivery_location": admin.VERTICAL,
        "gm_treated": admin.VERTICAL,
        "maternal_outcome": admin.VERTICAL,
    }

    search_fields = ("subject_identifier", "action_identifier", "tracking_identifier")

    @admin.display
    def birth_outcomes(self, obj=None, label=None):
        url = reverse("meta_prn_admin:meta_prn_birthoutcomes_changelist")
        url = f"{url}?q={obj.subject_identifier}"
        context = dict(title="Outcomes", url=url, label="Outcomes")
        return render_to_string("dashboard_button.html", context=context)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        action_flds.remove("action_identifier")
        fields = list(action_flds) + list(fields)
        return fields
