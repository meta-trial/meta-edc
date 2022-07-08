from django.contrib import admin, messages
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsRftForm
from ...models import BloodResultsRft, EgfrNotification
from ..modeladmin import CrfModelAdmin


@admin.register(BloodResultsRft, site=meta_subject_admin)
class BloodResultsRftAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):

    form = BloodResultsRftForm
    actions = ["create_or_update_egfr_notification"]
    fieldsets = (
        *BloodResultFieldset(
            BloodResultsRft.lab_panel,
            model_cls=BloodResultsRft,
            excluded_utest_ids=["egfr"],
        ).fieldsets,
        (
            "Calculated eGFR",
            {
                "classes": ("collapse",),
                "fields": ["egfr_value", "egfr_units", "egfr_percent_change"],
            },
        ),
    )

    readonly_fields = ["egfr_value", "egfr_units", "egfr_percent_change"]

    @admin.action(permissions=["view"], description="Create or update eGFR notification")
    def create_or_update_egfr_notification(self, request, queryset):
        total = EgfrNotification.objects.all().count()
        for obj in queryset:
            obj.save()
        new_total = EgfrNotification.objects.all().count()
        messages.success(request, f"Created {new_total - total} new eGFR notifications.")
