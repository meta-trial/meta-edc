from edc_constants.constants import OTHER, UNKNOWN

from .constants import HOSPITAL_CLINIC

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
