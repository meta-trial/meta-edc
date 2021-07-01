from django.contrib import admin
from edc_blood_results.admin import BloodResultsModelAdminMixin
from edc_blood_results.fieldsets import BloodResultPanel
from edc_lab_panel.panels import blood_glucose_panel

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsGluForm
from ...models import BloodResultsGlu
from ..modeladmin import CrfModelAdmin

# TODO: add is poc?


@admin.register(BloodResultsGlu, site=meta_subject_admin)
class BloodResultsGluAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsGluForm
    fieldsets = BloodResultPanel(blood_glucose_panel).fieldsets


#
#
#
# from django.contrib import admin
# from edc_model_admin import audit_fieldset_tuple
#
# from ...admin_site import meta_subject_admin
# from ...forms import BloodResultsGluForm
# from ...models import BloodResultsGlu
# from .blood_results_modeladmin_mixin import (
#     BloodResultsModelAdminMixin,
#     conclusion_fieldset,
#     summary_fieldset,
# )
#
#
# @admin.register(BloodResultsGlu, site=meta_subject_admin)
# class BloodResultsGluAdmin(BloodResultsModelAdminMixin):
#
#     form = BloodResultsGluForm
#
#     autocomplete_fields = ["glucose_requisition"]
#
#     fieldsets = (
#         (None, {"fields": ("subject_visit", "report_datetime")}),
#         (
#             "Blood Glucose",
#             {
#                 "fields": [
#                     "is_poc",
#                     "blood_glucose_requisition",
#                     "blood_glucose_assay_datetime",
#                     "fasting",
#                     "blood_glucose_value",
#                     "blood_glucose_units",
#                     "blood_glucose_abnormal",
#                     "blood_glucose_reportable",
#                 ]
#             },
#         ),
#         conclusion_fieldset,
#         summary_fieldset,
#         audit_fieldset_tuple,
#     )
#
#     radio_fields = {
#         "is_poc": admin.VERTICAL,
#         "fasting": admin.VERTICAL,
#         "results_abnormal": admin.VERTICAL,
#         "results_reportable": admin.VERTICAL,
#     }
