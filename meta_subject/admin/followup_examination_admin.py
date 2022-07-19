from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import (
    ActionItemModelAdminMixin,
    action_fields,
    action_fieldset_tuple,
)
from edc_constants.constants import NONE, YES
from edc_crf.fieldset import crf_status_fieldset
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import FollowupExaminationForm
from ..models import FollowupExamination
from .modeladmin import CrfModelAdminMixin


class GradedEventFilter(admin.SimpleListFilter):
    title = _("Graded events")
    parameter_name = "grade"

    def lookups(self, request, model_admin):
        return (
            ("g3", _("Grade 3")),
            ("g4", _("Grade 4")),
        )

    def queryset(self, request, queryset):
        if self.value() == "g3":
            return queryset.exclude(symptoms_g3__name=NONE)
        if self.value() == "g4":
            return queryset.exclude(symptoms_g4__name=NONE)


@admin.register(FollowupExamination, site=meta_subject_admin)
class FollowupExaminationAdmin(
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = FollowupExaminationForm

    autocomplete_fields = ["art_new_regimen"]

    additional_instructions = [
        "If participant is pregnant, complete the action linked CRF `Pregnancy notification`."
    ]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Part 1: Symptoms",
            {
                "description": "To be completed by the study physician",
                "fields": (
                    "symptoms",
                    "symptoms_detail",
                    "symptoms_g3",
                    "symptoms_g3_detail",
                    "symptoms_g4",
                    "symptoms_g4_detail",
                ),
            },
        ),
        (
            "Part 2: Other Medical or Health problems",
            {
                "description": "To be completed by the study physician",
                "fields": (
                    "any_other_problems",
                    "any_other_problems_detail",
                    "any_other_problems_sae",
                    "any_other_problems_sae_grade",
                ),
            },
        ),
        (
            "Part 3: Hospitalizations or other external access to care",
            {
                "description": "To be completed by the study physician",
                "fields": (
                    "attended_clinic",
                    "admitted_hospital",
                    "attended_clinic_detail",
                    "attended_clinic_sae",
                    "prescribed_medication",
                    "prescribed_medication_detail",
                ),
            },
        ),
        (
            "Part 4: HIV Medications",
            {
                "description": "To be completed by the study physician",
                "fields": (
                    "art_change",
                    "art_change_reason",
                    "art_new_regimen",
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
        crf_status_fieldset,
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = ("symptoms", "symptoms_g3", "symptoms_g4")

    readonly_fields = action_fields

    radio_fields = {
        "abdominal_tenderness": admin.VERTICAL,
        "admitted_hospital": admin.VERTICAL,
        "any_other_problems": admin.VERTICAL,
        "any_other_problems_sae": admin.VERTICAL,
        "any_other_problems_sae_grade": admin.VERTICAL,
        "art_change": admin.VERTICAL,
        "art_new_regimen": admin.VERTICAL,
        "attended_clinic": admin.VERTICAL,
        "attended_clinic_sae": admin.VERTICAL,
        "enlarged_liver": admin.VERTICAL,
        "hepatomegaly": admin.VERTICAL,
        "jaundice": admin.VERTICAL,
        "lactic_acidosis": admin.VERTICAL,
        "prescribed_medication": admin.VERTICAL,
        "referral": admin.VERTICAL,
    }

    list_display = ("g3", "g4")

    list_filter = (GradedEventFilter,)

    def g3(self, obj=None):
        if NONE not in [o.name for o in obj.symptoms_g3.all()]:
            return YES
        return None

    def g4(self, obj=None):
        if NONE not in [o.name for o in obj.symptoms_g4.all()]:
            return YES
        return None
