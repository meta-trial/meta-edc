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


def get_part_one_fieldset(collapse=None):

    dct = {
        "description": mark_safe(
            "To be completed by the <u>study clinician</u> or the "
            "<u>research nurse</u> in consultation with the study clinician"
        ),
        "fields": part_one_fields,
    }
    if collapse:
        dct.update(classes=("collapse",))
    return ("Part 1", dct)


def get_part_two_fieldset(collapse=None):
    dct = {
        "description": mark_safe(
            "To be completed by the <u>study clinician</u> or the "
            "<u>research nurse</u> in consultation with the study clinician"
        ),
        "fields": part_two_fields,
    }
    if collapse:
        dct.update(classes=("collapse",))
    return ("Part 2", dct)


def get_part_three_fieldset(collapse=None):
    dct = {
        "description": mark_safe("To be completed by the <u>study clinician</u>"),
        "fields": part_three_fields,
    }
    if collapse:
        dct.update(classes=("collapse",))
    return ("Part 3: Biomedical Indicators", dct)


def get_part_three_glucose_fieldset(collapse=None):
    dct = {"fields": part_three_glucose_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return ("Part 3a: Glucose", dct)


def get_part_three_other_fieldset(collapse=None):
    dct = {"fields": part_three_other_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return ("Part 3b: Creatinine / HbA1c", dct)


def get_part_three_vitals_fieldset(collapse=None):
    dct = {"fields": part_three_vitals_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return ("Part 3c: Vitals", dct)


def get_part_three_pregnancy_fieldset(collapse=None):
    dct = {"fields": part_three_pregnancy_fields}
    if collapse:
        dct.update(classes=("collapse",))
    return ("Part 3d: Pregnancy", dct)


comments_fieldset = (
    "Additional Comments",
    {"fields": (*part_three_comment_fields,),},
)

calculated_values_fieldset = (
    "Calculated values",
    {
        "classes": ("collapse",),
        "fields": (
            "calculated_bmi",
            "converted_fasting_glucose",
            "converted_ogtt_two_hr",
            "converted_creatinine",
            "calculated_egfr",
            "inclusion_a",
            "inclusion_b",
            "inclusion_c",
            "inclusion_d",
        ),
    },
)
