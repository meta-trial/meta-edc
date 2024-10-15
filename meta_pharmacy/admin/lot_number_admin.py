from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_model_admin.mixins import (
    ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin,
    ModelAdminRedirectOnDeleteMixin,
    TemplatesModelAdminMixin,
)

from ..admin_site import meta_pharmacy_admin
from ..models import LotNumber
from .actions import prepare_label_data


@admin.register(LotNumber, site=meta_pharmacy_admin)
class LotNumberAdmin(
    TemplatesModelAdminMixin,
    ModelAdminNextUrlRedirectMixin,  # add
    ModelAdminFormInstructionsMixin,  # add
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,  # add
    ModelAdminInstitutionMixin,  # add
    ModelAdminRedirectOnDeleteMixin,
    admin.ModelAdmin,
):
    """Admin class for proxy model of edc_pharmacy.Rx"""

    show_object_tools = True

    actions = [prepare_label_data]

    # form = LotNumberForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "medication",
                    "lot_no",
                    "expiration_date",
                    "assignment",
                    "qty",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "medication",
        "lot_no",
        "expiration_date",
        "assignment",
    )

    radio_fields = {"assignment": admin.VERTICAL}

    list_filter = ("assignment",)

    search_fields = [
        "lot_no",
    ]
