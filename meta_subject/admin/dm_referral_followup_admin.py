from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_adherence.model_admin_mixin import get_visual_score_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms.dm_referral_followup import DmReferralFollowupForm
from ..models import DmReferralFollowup
from .modeladmin import CrfModelAdminMixin


@admin.register(DmReferralFollowup, site=meta_subject_admin)
class DmReferralFollowupAdmin(
    CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin
):
    form = DmReferralFollowupForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Diabetes clinic attendance",
            {
                "fields": (
                    "attended",
                    "not_attended_reason",
                    "facility_attended",
                    "attended_date",
                    "healthcare_workers",
                    "other_healthcare_workers",
                ),
            },
        ),
        (
            "Investigations",
            {
                "fields": (
                    "investigations_performed",
                    "investigations",
                    "other_investigations",
                    "complications_checks",
                ),
            },
        ),
        (
            "Diabetes treatment",
            {
                "fields": (
                    "dm_treatments",
                    "on_dm_medications",
                    "dm_medications_init_date",
                    "dm_medications",
                    "other_dm_medications",
                ),
            },
        ),
        (
            "Diabetes Medication Adherence",
            {
                "fields": (
                    "medications_adherent",
                    "last_missed_pill",
                ),
            },
        ),
        get_visual_score_fieldset_tuple(),
        crf_status_fieldset,
        audit_fieldset_tuple,
    )

    filter_horizontal = (
        "healthcare_workers",
        "investigations",
        "complications_checks",
        "dm_treatments",
        "dm_medications",
    )

    radio_fields = {
        "attended": admin.VERTICAL,
        "investigations_performed": admin.VERTICAL,
        "on_dm_medications": admin.VERTICAL,
        "medications_adherent": admin.VERTICAL,
        "last_missed_pill": admin.VERTICAL,
    }
