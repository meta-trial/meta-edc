from typing import Tuple

from django.utils.safestring import mark_safe

from ..forms import (
    part_one_fields,
    part_three_comment_fields,
    part_three_fields,
    part_three_glucose_fields,
    part_three_other_fields,
    part_three_pregnancy_fields,
    part_three_vitals_fields,
    part_two_fields,
)
from ..forms.field_lists import (
    part_three_creatinine_fields,
    part_three_hba1c_fields,
    part_three_repeat_fbg_fields,
    part_three_repeat_ogtt_fields,
)


def get_part_one_fieldset(collapse=None) -> Tuple[str, dict]:

    dct = {
        "description": mark_safe(  # nosec B308
            "To be completed by the <u>study clinician</u> or the "
            "<u>research nurse</u> in consultation with the study clinician"
        ),
        "fields": part_one_fields,
    }
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 1", dct


def get_part_two_fieldset(collapse=None) -> Tuple[str, dict]:
    dct = {
        "description": mark_safe(  # nosec B308
            "To be completed by the <u>study clinician</u> or the "
            "<u>research nurse</u> in consultation with the study clinician"
        ),
        "fields": part_two_fields,
    }
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 2", dct


def get_part_three_fieldset(
    collapse=None,
) -> Tuple[str, dict]:
    dct = {
        "description": mark_safe(  # nosec B308
            "To be completed by the <u>study clinician</u>"
        ),
        "fields": part_three_fields,
    }
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3: Biomedical Indicators", dct


def get_part_three_glucose_fieldset(collapse=None):
    dct = {"fields": part_three_glucose_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3c:  Glucose Measurements (FBG / OGTT)", dct


def get_part_three_repeat_glucose_fieldset(collapse=None) -> Tuple[str, dict]:
    fields = [
        "repeat_glucose_performed",
        "repeat_fasting",
        "repeat_fasting_duration_str",
    ]
    fields.extend(part_three_repeat_fbg_fields)
    fields.extend(part_three_repeat_ogtt_fields)
    dct = {
        "fields": fields,
        "description": (
            "IMPORTANT: If you decide to repeat the FBG / OGTT, do so at least "
            "three days after the first FBG / OGTT"
        ),
    }
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3d: Repeat Glucose Measurements (FBG / OGTT)", dct


def get_part_three_other_fieldset(collapse=None) -> Tuple[str, dict]:
    dct = {"fields": part_three_other_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3e: Creatinine / HbA1c", dct


def get_part_three_creatinine_fieldset(collapse=None) -> Tuple[str, dict]:
    dct = {"fields": part_three_creatinine_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3e: Creatinine", dct


def get_part_three_hba1c_fieldset(collapse=None) -> Tuple[str, dict]:
    dct = {"fields": part_three_hba1c_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3f: HbA1c", dct


def get_part_three_report_datetime_fieldset() -> Tuple[str, dict]:
    dct = {"fields": ["part_three_report_datetime"]}
    return "Part 3", dct


def get_part_three_vitals_fieldset(collapse=None) -> Tuple[str, dict]:
    dct = {"fields": part_three_vitals_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3a: Vitals", dct


def get_part_three_pregnancy_fieldset(collapse=None) -> Tuple[str, dict]:
    dct = {"fields": part_three_pregnancy_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3b: Pregnancy", dct


def get_p3_screening_appt_update_fields(collapse=None) -> Tuple[str, dict]:
    dct = {
        "description": mark_safe(  # nosec B308
            '<span style="color:orange;font-weight:bold">IMPORTANT:</span>'
            "This section is only applicable if the subject "
            "missed the appointment for the second stage of screening (P3). "
            "If the subject appears for screening after this sections has "
            "been completed, you may, of course, proceed to screen "
            "the subject as per protocol."
        ),
        "fields": ["p3_ltfu", "p3_ltfu_date", "p3_ltfu_comment"],
    }
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3 screening appointment update", dct


comments_fieldset: Tuple[str, dict] = (
    "Additional Comments",
    {
        "fields": (*part_three_comment_fields,),
    },
)

calculated_values_fieldset: Tuple[str, dict] = (
    "Calculated values",
    {
        "classes": ("collapse",),
        "fields": (
            "sys_blood_pressure_avg",
            "dia_blood_pressure_avg",
            "converted_fbg_value",
            "converted_ogtt_value",
            "converted_fbg2_value",
            "converted_ogtt2_value",
            "converted_creatinine_value",
            "calculated_egfr_value",
        ),
    },
)
