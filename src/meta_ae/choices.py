from clinicedc_constants import OTHER, PENDING, UNKNOWN

from .constants import AGREED, HOSPITAL_CLINIC, REQUIRES_REVIEW

AE_TYPE = (
    ("sae", "Serious Adverse Event / Reaction"),
    ("aesi", "Adverse Event of Special Interest"),
    ("susar", "Serious Unexpected Adverse Reaction"),
)

AE_EXPECTED = (
    ("expected", "Expected"),
    ("unexpected", "Unexpected"),
)

AE_ACTION_REQUIRED = (
    ("action", "Further action is required"),
    ("no_action", "No further action is required"),
)

DEATH_LOCATIONS = (
    ("home", "At home"),
    (HOSPITAL_CLINIC, "Hospital/clinic"),
    ("elsewhere", "Elsewhere"),
)


INFORMANT_RELATIONSHIP = (
    ("husband_wife", "Husband/wife"),
    ("Parent", "Parent"),
    ("child", "Child"),
    (UNKNOWN, "Unknown"),
    (OTHER, "Other"),
)

REVIEW_STATUS = (
    (PENDING, "Pending: awaiting the AE TMG report"),
    (AGREED, "Agreed: the original and TMG classifications agree"),
    (REQUIRES_REVIEW, "Requires review: the classifications do not agree"),
)
