from edc_reportable import GRADE3, GRADE4, site_reportables
from edc_reportable.grading_data.daids_july_2017 import chemistries, dummies, hematology
from edc_reportable.normal_data.africa import normal_data

grading_data = {}
grading_data.update(**dummies)
grading_data.update(**chemistries)
grading_data.update(**hematology)

site_reportables.register(
    name="meta",
    normal_data=normal_data,
    grading_data=grading_data,
    reportable_grades=[GRADE3, GRADE4],
    reportable_grades_exceptions=None,
)
