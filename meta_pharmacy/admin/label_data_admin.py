from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
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
from ..forms import LabelBatchForm
from ..models import LabelData
from .actions import print_label_sheet


@admin.register(LabelData, site=meta_pharmacy_admin)
class LabelDataAdmin(
    TemplatesModelAdminMixin,
    ModelAdminNextUrlRedirectMixin,  # add
    ModelAdminFormInstructionsMixin,  # add
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,  # add
    ModelAdminInstitutionMixin,  # add
    ModelAdminRedirectOnDeleteMixin,
    admin.ModelAdmin,
):
    actions = [print_label_sheet]

    form = LabelBatchForm

    list_display = (
        "subject_identifier",
        "reference",
        "sid",
        "site_id",
        "batch",
        "printed",
        "scanned",
        "received",
        "dispensed",
        "crf",
        "created",
    )

    list_filter = (
        "printed",
        "scanned",
        "received",
        "dispensed",
        "crf",
        "created",
    )
    readonly_fields = (
        "subject_identifier",
        "gender",
        "sid",
        "reference",
        "label_batch",
        "site_name",
    )
    search_fields = (
        "label_batch__batch",
        "label_batch__lot_number__lot_no",
        "subject_identifier",
        "sid",
        "reference",
    )

    @admin.display(description="Label batch", ordering="label_batch__batch")
    def batch(self, obj):
        url = reverse("meta_pharmacy_admin:meta_pharmacy_labelbatch_changelist")
        url = f"{url}?q={obj.label_batch.batch}"
        return format_html(f'<A href="{url}">{obj.label_batch.batch}</A>')
