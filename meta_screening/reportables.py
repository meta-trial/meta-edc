from edc_constants.constants import FEMALE, MALE
from edc_reportable import NormalReference
from edc_reportable.units import MICROMOLES_PER_LITER


gluc_fasting_ref = NormalReference(
    name="gluc",
    lower=6.1,
    upper=6.9,
    lower_inclusive=True,
    upper_inclusive=True,
    units=MICROMOLES_PER_LITER,
    gender=[MALE, FEMALE],
    age_lower=18,
    age_lower_inclusive=True,
)

gluc_2hr_ref = NormalReference(
    name="gluc_2hr",
    lower=7.00,
    upper=11.10,
    lower_inclusive=True,
    upper_inclusive=True,
    units=MICROMOLES_PER_LITER,
    gender=[MALE, FEMALE],
    age_lower=18,
    age_lower_inclusive=True,
)
