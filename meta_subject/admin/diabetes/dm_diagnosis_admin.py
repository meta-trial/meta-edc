from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_model_admin.mixins import TabularInlineMixin

from ...admin_site import meta_subject_admin
from ...forms import DmDiagnosisForm, DmDxResultForm
from ...models import DmDiagnosis, DmDxResult
from ..modeladmin import CrfModelAdminMixin


class DmDxResultInline(
    TabularInlineMixin,
    admin.TabularInline,
):

    form = DmDxResultForm
    extra = 1
    view_on_site = False
    min_num = 1
    insert_before_fieldset = "Comments"
    verbose_name_plural = "Results used in the decision to diagnose"

    fieldsets = (
        [
            "Lab results",
            {
                "description": "List the lab results used for this decision",
                "fields": (
                    "report_date",
                    "utestid",
                    "value",
                    "fasted",
                    "comment",
                ),
            },
        ],
    )

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset

    model = DmDxResult
    form = DmDxResultForm


@admin.register(DmDiagnosis, site=meta_subject_admin)
class DmDiagnosisAdmin(
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = DmDiagnosisForm

    inlines = [DmDxResultInline]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Diagnosis",
            {
                "fields": (
                    "dx_date",
                    "dx_initiated_by",
                    "dx_initiated_by_other",
                    "dx_tmg",
                    "dx_tmg_date",
                    "dx_no_tmg_reason",
                ),
            },
        ),
        (
            "Comments",
            {
                "fields": ("comments",),
            },
        ),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "dx_initiated_by": admin.VERTICAL,
        "dx_tmg": admin.VERTICAL,
    }
