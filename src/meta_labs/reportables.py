from clinicedc_constants import (
    FEMALE,
    MALE,
    MICRO_IU_MILLILITER,
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
)
from edc_reportable.adult_age_options import adult_age_options
from edc_reportable.data import africa, daids_july_2017
from edc_reportable.formula import Formula

grading_data = {}
grading_data.update(**daids_july_2017.dummies)
grading_data.update(**daids_july_2017.chemistries)
grading_data.update(**daids_july_2017.hematology)

collection_name = "meta"
normal_data = africa.normal_data
reportable_grades = [3, 4]
reportable_grades_exceptions = {}

normal_data.update(
    {
        "glucose": [
            Formula(
                "0<=x<=99999",
                units=MILLIMOLES_PER_LITER,
                gender=[MALE, FEMALE],
                **adult_age_options,
            ),
            Formula(
                "0<=x<=99999",
                units=MILLIGRAMS_PER_DECILITER,
                gender=[MALE, FEMALE],
                **adult_age_options,
            ),
        ],
        "ins": [
            Formula(
                "0<=x<=99999",
                units=MICRO_IU_MILLILITER,
                gender=[MALE, FEMALE],
                **adult_age_options,
            ),
        ],
    }
)

grading_data.update(
    {
        "glucose": [
            Formula(
                "x<0",
                grade=0,
                units=MILLIMOLES_PER_LITER,
                gender=[MALE, FEMALE],
                **adult_age_options,
            ),
            Formula(
                "x<0",
                grade=0,
                units=MILLIGRAMS_PER_DECILITER,
                gender=[MALE, FEMALE],
                **adult_age_options,
            ),
        ],
        "ins": [
            Formula(
                "x<0",
                grade=0,
                units=MICRO_IU_MILLILITER,
                gender=[MALE, FEMALE],
                **adult_age_options,
            ),
        ],
    }
)

reference_range_options = dict(
    collection_name=collection_name,
    normal_data=africa.normal_data,
    grading_data=grading_data,
    reportable_grades=reportable_grades,
    reportable_grades_exceptions=reportable_grades_exceptions,
)
