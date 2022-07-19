from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from edc_action_item import (
    ActionItemModelAdminMixin,
    action_fields,
    action_fieldset_tuple,
)
from edc_crf.fieldset import crf_status_fieldset
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin, TabularInlineMixin, audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import BirthOutcomesForm, DeliveryForm
from ..models import BirthOutcomes, Delivery
from .modeladmin import CrfModelAdminMixin


class BirthOutcomesInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = BirthOutcomes
    form = BirthOutcomesForm
    extra = 1
    fields = [
        "birth_order",
        "birth_outcome",
        "birth_weight",
    ]


@admin.register(Delivery, site=meta_subject_admin)
class DeliveryAdmin(
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = DeliveryForm

    inlines = [BirthOutcomesInlineAdmin]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Source of information",
            {
                "fields": (
                    "info_available",
                    "info_not_available_reason",
                    "info_source",
                    "info_source_other",
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
        crf_status_fieldset,
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    list_display = (
        "subject_visit",
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
        "info_available": admin.VERTICAL,
        "info_source": admin.VERTICAL,
        "informant_relation": admin.VERTICAL,
        "delivery_time_estimated": admin.VERTICAL,
        "delivery_location": admin.VERTICAL,
        "gm_treated": admin.VERTICAL,
        "maternal_outcome": admin.VERTICAL,
    }

    readonly_fields = action_fields

    search_fields = (
        "subject_visit__subject_identifier",
        "action_identifier",
        "tracking_identifier",
    )

    @admin.display
    def birth_outcomes(self, obj=None, label=None):
        url = reverse("meta_subject_admin:meta_subject_birthoutcomes_changelist")
        url = f"{url}?q={obj.subject_identifier}"
        context = dict(title="Outcomes", url=url, label="Outcomes")
        return render_to_string("dashboard_button.html", context=context)
