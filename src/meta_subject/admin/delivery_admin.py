from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.template.loader import render_to_string
from django.urls import reverse
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fields, action_fieldset_tuple
from edc_action_item.modeladmin_mixins import ActionItemModelAdminMixin
from edc_crf.fieldset import crf_status_fieldset
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.mixins import TabularInlineMixin

from ..admin_site import meta_subject_admin
from ..forms import BirthOutcomesForm, DeliveryForm
from ..models import BirthOutcomes, Delivery
from .modeladmin import CrfModelAdminMixin


class BirthOutcomesInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # instance here is the parent Delivery instance
        delivery = self.instance
        expected = delivery.fetal_outcome_count

        if expected is None:
            return  # let field-level validation handle a missing value

        # count forms that are valid, not marked for deletion, and not empty
        valid_count = 0
        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            if form.cleaned_data.get("DELETE", False):
                continue
            if form.cleaned_data.get("id") is None and not form.has_changed():
                continue  # skip blank extra forms
            valid_count += 1

        if valid_count != expected:
            raise ValidationError(
                f"Delivery indicates {expected} birth outcome(s) expected, "
                f"but {valid_count} were entered."
            )


class BirthOutcomesInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = BirthOutcomes
    form = BirthOutcomesForm
    formset = BirthOutcomesInlineFormSet
    extra = 1
    fields = (
        "birth_order",
        "birth_outcome",
        "birth_weight",
    )


@admin.register(Delivery, site=meta_subject_admin)
class DeliveryAdmin(
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = DeliveryForm

    inlines = (BirthOutcomesInlineAdmin,)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "report_available",
                    "report_not_available_reason",
                )
            },
        ),
        (
            "Source of information",
            {
                "fields": (
                    "info_source",
                    "info_source_other",
                    "informant_relation",
                    "informant_relation_other",
                ),
            },
        ),
        (
            "Delivery report",
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

    radio_fields = {  # noqa: RUF012
        "report_available": admin.VERTICAL,
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
    )

    @admin.display
    def birth_outcomes(self, obj=None, label=None):  # noqa: ARG002
        url = reverse("meta_subject_admin:meta_subject_birthoutcomes_changelist")
        url = f"{url}?q={obj.subject_identifier}"
        context = dict(title="Outcomes", url=url, label="Outcomes")
        return render_to_string("edc_subject_dashboard/dashboard_button.html", context=context)
