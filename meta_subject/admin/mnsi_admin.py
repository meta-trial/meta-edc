from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms.mnsi_form import MnsiForm
from ..models import Mnsi
from .modeladmin import CrfModelAdminMixin


@admin.register(Mnsi, site=meta_subject_admin)
class MnsiAdmin(
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = MnsiForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "mnsi_performed",
                    "mnsi_not_performed_reason",
                )
            },
        ),
        (
            "Part 1: Patient History",
            {
                "description": "History (To be completed by the person with diabetes)",
                "fields": (
                    "numb_legs_feet",
                    "burning_pain_legs_feet",
                    "feet_sensitive_touch",
                    "muscle_cramps_legs_feet",
                    "prickling_feelings_legs_feet",
                    "covers_touch_skin_painful",
                    "differentiate_hot_cold_water",
                    "open_sore_foot_history",
                    "diabetic_neuropathy",
                    "feel_weak",
                    "symptoms_worse_night",
                    "legs_hurt_when_walk",
                    "sense_feet_when_walk",
                    "skin_cracks_open_feet",
                    "amputation",
                ),
            },
        ),
        (
            "Part 2a: Physical Assessment - Right Foot",
            {
                "description": (
                    "Right Foot Physical Assessment (To be completed by health professional)"
                ),
                "fields": (
                    "examined_right_foot",
                    "normal_appearance_right_foot",
                    "abnormal_obs_right_foot",
                    "abnormal_obs_right_foot_other",
                    "ulceration_right_foot",
                    "ankle_reflexes_right_foot",
                    "vibration_perception_right_toe",
                    "monofilament_right_foot",
                ),
            },
        ),
        (
            "Part 2b: Physical Assessment - Left Foot",
            {
                "description": (
                    "Left Foot Physical Assessment (To be completed by health professional)"
                ),
                "fields": (
                    "examined_left_foot",
                    "normal_appearance_left_foot",
                    "abnormal_obs_left_foot",
                    "abnormal_obs_left_foot_other",
                    "ulceration_left_foot",
                    "ankle_reflexes_left_foot",
                    "vibration_perception_left_toe",
                    "monofilament_left_foot",
                ),
            },
        ),
        (
            "Calculated values",
            {
                "classes": ("collapse",),
                "fields": (
                    "calculated_patient_history_score",
                    "calculated_physical_assessment_score",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = (
        "abnormal_obs_left_foot",
        "abnormal_obs_right_foot",
    )

    readonly_fields = (
        "calculated_patient_history_score",
        "calculated_physical_assessment_score",
    )

    radio_fields = {
        "amputation": admin.VERTICAL,
        "ankle_reflexes_left_foot": admin.VERTICAL,
        "ankle_reflexes_right_foot": admin.VERTICAL,
        "burning_pain_legs_feet": admin.VERTICAL,
        "covers_touch_skin_painful": admin.VERTICAL,
        "diabetic_neuropathy": admin.VERTICAL,
        "differentiate_hot_cold_water": admin.VERTICAL,
        "examined_left_foot": admin.VERTICAL,
        "examined_right_foot": admin.VERTICAL,
        "feel_weak": admin.VERTICAL,
        "feet_sensitive_touch": admin.VERTICAL,
        "legs_hurt_when_walk": admin.VERTICAL,
        "monofilament_left_foot": admin.VERTICAL,
        "monofilament_right_foot": admin.VERTICAL,
        "muscle_cramps_legs_feet": admin.VERTICAL,
        "normal_appearance_left_foot": admin.VERTICAL,
        "normal_appearance_right_foot": admin.VERTICAL,
        "numb_legs_feet": admin.VERTICAL,
        "open_sore_foot_history": admin.VERTICAL,
        "prickling_feelings_legs_feet": admin.VERTICAL,
        "sense_feet_when_walk": admin.VERTICAL,
        "skin_cracks_open_feet": admin.VERTICAL,
        "symptoms_worse_night": admin.VERTICAL,
        "ulceration_left_foot": admin.VERTICAL,
        "ulceration_right_foot": admin.VERTICAL,
        "vibration_perception_left_toe": admin.VERTICAL,
        "vibration_perception_right_toe": admin.VERTICAL,
    }
