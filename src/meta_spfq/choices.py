from django.utils.translation import gettext as _

from .constants import (
    EXTREME,
    HIGHLY,
    MODERATE,
    MODERATELY,
    MUCH_LESS_EXPECTED,
    MUCH_MORE_EXPECTED,
    NOT_AT_ALL,
    SAME_AS_EXPECTED,
    SEVERE,
    SLIGHT,
    SLIGHTLY,
    SOMEWHAT_LESS_EXPECTED,
    SOMEWHAT_MORE_EXPECTED,
    VERY_HIGHLY,
)

NOT_AT_ALL_TO_SEVERE_CHOICE = (
    (NOT_AT_ALL, _("Not at all")),
    (SLIGHT, _("Slight")),
    (MODERATE, _("Moderate")),
    (EXTREME, _("Extreme")),
    (SEVERE, _("Severe")),
)

NOT_AT_ALL_TO_HIGHLY_CHOICE = (
    (NOT_AT_ALL, _("Not at all")),
    (SLIGHTLY, _("Slightly")),
    (MODERATELY, _("Moderately")),
    (HIGHLY, _("Highly")),
    (VERY_HIGHLY, _("Very highly")),
)
LESS_EXPECTED_TO_MORE_EXPECTED_CHOICE = (
    (MUCH_LESS_EXPECTED, _("Much less than expected")),
    (SOMEWHAT_LESS_EXPECTED, _("Somewhat less than expected")),
    (SAME_AS_EXPECTED, _("Same as expected")),
    (SOMEWHAT_MORE_EXPECTED, _("Somewhat more than expected")),
    (MUCH_MORE_EXPECTED, _("Much more than expected")),
)
