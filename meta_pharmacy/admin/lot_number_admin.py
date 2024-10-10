from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import meta_pharmacy_admin
from ..models import LotNumber


@admin.register(LotNumber, site=meta_pharmacy_admin)
class LotNumberAdmin(ModelAdminSubjectDashboardMixin, admin.ModelAdmin):
    """Admin class for proxy model of edc_pharmacy.Rx"""

    show_object_tools = True

    # form = LotNumberForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "lot_no",
                    "expiration_date",
                    "allocation",
                    "qty",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "lot_no",
        "expiration_date",
    )

    radio_fields = {"allocation": admin.VERTICAL}

    list_filter = ("allocation",)

    search_fields = [
        "lot_no",
    ]
