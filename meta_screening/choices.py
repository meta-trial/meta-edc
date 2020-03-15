from edc_reportable import (
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MICROMOLES_PER_LITER,
    MICROMOLES_PER_LITER_DISPLAY,
)
from edc_constants.constants import (
    BLACK,
    OTHER,
    NOT_APPLICABLE,
    YES,
    NO,
)


ETHNICITY = ((BLACK, "Black"), (OTHER, "Other"))

GLUCOSE_UNITS = (
    (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
    (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER),
)

REFUSAL_REASONS = (
    ("dont_have_time", "I don't have time"),
    ("must_consult_spouse", "I need to consult my spouse"),
    ("dont_want_blood_drawn", "I don't want to have the blood drawn"),
    ("dont_want_to_join", "I don't want to take part"),
    ("need_to_think_about_it", "I haven't had a chance to think about it"),
    (OTHER, "Other, please specify"),
)

SERUM_CREATININE_UNITS = (
    (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
    (MICROMOLES_PER_LITER, MICROMOLES_PER_LITER_DISPLAY),
)


YES_NO_NOT_ELIGIBLE = (
    (YES, YES),
    (NO, NO),
    (
        NOT_APPLICABLE,
        ("Not applicable, subject is not eligible based on the criteria above"),
    ),
)
