from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import meta_subject_admin
from ...forms import DmEndpointForm
from ...models import DmEndpoint
from ..modeladmin import CrfModelAdminMixin


@admin.register(DmEndpoint, site=meta_subject_admin)
class DmEndpointAdmin(
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = DmEndpointForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Endpoint reached",
            {
                "fields": ("endpoint_reached", "comments"),
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    list_filter = ("endpoint_reached",)

    radio_fields = {"endpoint_reached": admin.VERTICAL}  # noqa: RUF012
