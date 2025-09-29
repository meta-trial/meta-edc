from edc_constants.constants import BLACK, NO, NOT_APPLICABLE, OTHER, PENDING, YES

ETHNICITY = ((BLACK, "Black"), (OTHER, "Other"))

REFUSAL_REASONS = (
    ("dont_have_time", "I don't have time"),
    ("must_consult_spouse", "I need to consult my spouse"),
    ("dont_want_blood_drawn", "I don't want to have the blood drawn"),
    ("dont_want_to_join", "I don't want to take part"),
    ("need_to_think_about_it", "I haven't had a chance to think about it"),
    (OTHER, "Other, please specify"),
)


YES_NO_NOT_ELIGIBLE = (
    (YES, YES),
    (NO, NO),
    (
        NOT_APPLICABLE,
        "Not applicable, subject is not eligible based on the criteria above",
    ),
)

YES_PENDING_NA = (
    (YES, YES),
    (PENDING, "Decision pending"),
    (NOT_APPLICABLE, "Not applicable"),
)
