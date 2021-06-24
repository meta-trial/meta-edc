from edc_reportable import site_reportables
from respond_labs.reportables import grading_data, normal_data

site_reportables.register(
    name="meta", normal_data=normal_data, grading_data=grading_data
)
