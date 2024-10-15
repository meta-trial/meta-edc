from django.contrib import admin
from django_labels.actions import copy_label_specification, export_to_csv
from django_labels.models import LabelSpecification
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
from .actions import print_test_label_sheet

admin.site.unregister(LabelSpecification)


@admin.register(LabelSpecification, site=meta_pharmacy_admin)
class LabelSpecificationAdmin(
    TemplatesModelAdminMixin,
    ModelAdminNextUrlRedirectMixin,  # add
    ModelAdminFormInstructionsMixin,  # add
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,  # add
    ModelAdminInstitutionMixin,  # add
    ModelAdminRedirectOnDeleteMixin,
    admin.ModelAdmin,
):
    actions = [print_test_label_sheet, copy_label_specification, export_to_csv]

    date_hierarchy = "created"

    list_display = (
        "name",
        "page_description",
        "layout_description",
        "label_description",
        "border",
    )

    readonly_fields = (
        "page_description",
        "layout_description",
        "label_description",
    )

    list_filter = ("created", "modified")
