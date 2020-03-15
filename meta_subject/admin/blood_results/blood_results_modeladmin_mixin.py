from django.contrib import admin
from edc_action_item import action_fields

from ..modeladmin import CrfModelAdmin


conclusion_fieldset = (
    "Conclusion",
    {"fields": ("results_abnormal", "results_reportable")},
)
summary_fieldset = ("Summary", {"classes": ("collapse",), "fields": ("summary",)})


class BloodResultsModelAdminMixin(CrfModelAdmin):

    form = None

    fieldsets = None

    radio_fields = {
        "results_abnormal": admin.VERTICAL,
        "results_reportable": admin.VERTICAL,
    }

    readonly_fields = ("summary",) + action_fields

    list_display = ("abnormal", "reportable", "action_identifier")

    list_filter = ("results_abnormal", "results_reportable")

    search_fields = ("action_identifier", "subject_identifier", "tracking_identifier")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "appointment" and request.GET.get("appointment"):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                pk=request.GET.get("appointment", 0)
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
