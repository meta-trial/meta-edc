from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import FollowupVitalsForm
from ..models import FollowupVitals
from .fields import get_blood_pressure_fields, get_respiratory_o2_fields
from .modeladmin import CrfModelAdminMixin


@admin.register(FollowupVitals, site=meta_subject_admin)
class FollowupVitalsAdmin(CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin):
    form = FollowupVitalsForm

    additional_instructions = (
        "If participant is pregnant, complete the action linked CRF `Pregnancy notification`."
    )

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Weight",
            {
                "fields": ("weight",),
            },
        ),
        (
            "Waist circumference",
            {
                "description": (
                    "REQUIRED at 36 and 48 months. If not measured "
                    "at 36 and 48 months, provide the reason."
                ),
                "fields": (
                    "waist_circumference_measured",
                    "waist_circumference",
                    "waist_circumference_comment",
                ),
            },
        ),
        (
            "BP and heart rate",
            {
                "description": (
                    "To be completed by the research nurse. <BR>"
                    "Refer to SOP for blood pressure measurement procedure."
                ),
                "fields": (
                    *get_blood_pressure_fields(),
                    "heart_rate",
                    *get_respiratory_o2_fields(),
                ),
            },
        ),
        (
            "Temperature",
            {
                "fields": ("temperature",),
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    filter_horizontal = ()

    radio_fields = {  # noqa: RUF012
        "waist_circumference_measured": admin.VERTICAL,
        "severe_htn": admin.VERTICAL,
    }
