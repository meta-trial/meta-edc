from django.utils.safestring import mark_safe

from meta_edc.meta_version import PHASE_THREE, PHASE_TWO, get_meta_version

from ..forms import (
    get_part_one_fields,
    get_part_three_fields,
    get_part_three_vitals_fields,
    get_part_two_fields,
    part_three_comment_fields,
    part_three_glucose_fields,
    part_three_other_fields,
    part_three_pregnancy_fields,
)


def get_part_one_fieldset(collapse=None):

    dct = {
        "description": mark_safe(
            "To be completed by the <u>study clinician</u> or the "
            "<u>research nurse</u> in consultation with the study clinician"
        ),
        "fields": get_part_one_fields(),
    }
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 1", dct


def get_part_two_fieldset(collapse=None):
    dct = {
        "description": mark_safe(
            "To be completed by the <u>study clinician</u> or the "
            "<u>research nurse</u> in consultation with the study clinician"
        ),
        "fields": get_part_two_fields(),
    }
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 2", dct


def get_part_three_fieldset(collapse=None):
    dct = {
        "description": mark_safe("To be completed by the <u>study clinician</u>"),
        "fields": get_part_three_fields(),
    }
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3: Biomedical Indicators", dct


def get_part_three_glucose_fieldset(collapse=None):
    dct = {"fields": part_three_glucose_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3a: Glucose", dct


def get_part_three_other_fieldset(collapse=None):
    dct = {"fields": part_three_other_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3b: Creatinine / HbA1c", dct


def get_part_three_vitals_fieldset(collapse=None):
    dct = {"fields": get_part_three_vitals_fields()}
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3c: Vitals", dct


def get_part_three_pregnancy_fieldset(collapse=None):
    dct = {"fields": part_three_pregnancy_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return "Part 3d: Pregnancy", dct


comments_fieldset = (
    "Additional Comments",
    {
        "fields": (*part_three_comment_fields,),
    },
)

if get_meta_version() == PHASE_THREE:
    calculated_values_fieldset = (
        "Calculated values",
        {
            "classes": ("collapse",),
            "fields": (
                "sys_blood_pressure_avg",
                "dia_blood_pressure_avg",
                "converted_ifg_value",
                "converted_ogtt_value",
                "converted_creatinine_value",
                "calculated_egfr_value",
            ),
        },
    )
else:
    calculated_values_fieldset = (
        "Calculated values",
        {
            "classes": ("collapse",),
            "fields": (
                "calculated_bmi_value",
                "converted_ifg_value",
                "converted_ogtt_value",
                "converted_creatinine_value",
                "calculated_egfr_value",
                "inclusion_a",
                "inclusion_b",
                "inclusion_c",
                "inclusion_d",
            ),
        },
    )
