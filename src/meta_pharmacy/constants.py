from clinicedc_constants import OK

METFORMIN = "metformin"
REVIEW = "REVIEW"
MISSING_SUBJECT_IDENTIFIER = "MISSING_SUBJECT_IDENTIFIER"

SUBSTITUTION_STATUS = (
    (OK, "ok"),
    (MISSING_SUBJECT_IDENTIFIER, "Missing Subject ID"),
    (REVIEW, "review"),
)
