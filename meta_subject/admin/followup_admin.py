from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin


from ..admin_site import meta_subject_admin
from ..forms import FollowupForm
from ..models import Followup
from .modeladmin import CrfModelAdminMixin


@admin.register(Followup, site=meta_subject_admin)
class FollowupAdmin(CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin):

    form = FollowupForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Part 1: Symptoms / ARVs",
            {
                "description": "To be completed by the study physician",
                "fields": (
                    "symptoms",
                    "symptoms_detail",
                    "symptoms_g3",
                    "symptoms_g4",
                    "any_other_problems",
                    "any_other_problems_detail",
                    "any_other_problems_sae",
                    "attended_clinic",
                    "admitted_hospital",
                    "attended_clinic_detail",
                    "prescribed_medication",
                    "prescribed_medication_detail",
                    "attended_clinic_sae",
                    "art_change",
                    "art_change_reason",
                    "art_new_regimen_other",
                ),
            },
        ),
        (
            "Part 2: Examination",
            {
                "description": "To be completed by the study physician",
                "fields": ("abdominal_tenderness", "enlarged_liver", "jaundice"),
            },
        ),
        (
            "Part 3: Summary",
            {
                "description": "To be completed by the study physician",
                "fields": (
                    "comment",
                    "lactic_acidosis",
                    "hepatomegaly",
                    "referral",
                    "referral_reason",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = ("symptoms", "symptoms_g3", "symptoms_g4")

    radio_fields = {
        "abdominal_tenderness": admin.VERTICAL,
        "admitted_hospital": admin.VERTICAL,
        "any_other_problems": admin.VERTICAL,
        "any_other_problems_sae": admin.VERTICAL,
        "art_change": admin.VERTICAL,
        "attended_clinic": admin.VERTICAL,
        "attended_clinic_sae": admin.VERTICAL,
        "enlarged_liver": admin.VERTICAL,
        "hepatomegaly": admin.VERTICAL,
        "jaundice": admin.VERTICAL,
        "lactic_acidosis": admin.VERTICAL,
        "prescribed_medication": admin.VERTICAL,
        "referral": admin.VERTICAL,
    }
