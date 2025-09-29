from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_action_item.modeladmin_mixins import ActionItemModelAdminMixin
from edc_adherence.model_admin_mixin import get_visual_score_fieldset_tuple
from edc_crf.fieldset import crf_status_fieldset
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import meta_subject_admin
from ...forms import DmFollowupForm
from ...models import DmFollowup
from ..modeladmin import CrfModelAdminMixin


@admin.register(DmFollowup, site=meta_subject_admin)
class DmFollowupAdmin(
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = DmFollowupForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Referral to Diabetes clinic", {"fields": ("referral_date",)}),
        (
            "Diabetes clinic attendance",
            {
                "fields": (
                    "attended",
                    "facility_attended",
                    "missed_referral_reasons",
                    "other_missed_referral_reason",
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
                    "treatment_prescribed",
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
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = (
        "healthcare_workers",
        "investigations",
        "complications_checks",
        "dm_treatments",
        "dm_medications",
        "missed_referral_reasons",
    )

    radio_fields = {  # noqa: RUF012
        "attended": admin.VERTICAL,
        "investigations_performed": admin.VERTICAL,
        "on_dm_medications": admin.VERTICAL,
        "medications_adherent": admin.VERTICAL,
        "last_missed_pill": admin.VERTICAL,
        "treatment_prescribed": admin.VERTICAL,
    }
