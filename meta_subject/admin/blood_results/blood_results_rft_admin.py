from django.contrib import admin
from edc_blood_results.admin import BloodResultsModelAdminMixin
from edc_blood_results.fieldsets import BloodResultFieldset
from edc_lab_panel.panels import rft_panel

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsRftForm
from ...models import BloodResultsRft
from ..modeladmin import CrfModelAdmin


@admin.register(BloodResultsRft, site=meta_subject_admin)
class BloodResultsRftAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsRftForm
    fieldsets = BloodResultFieldset(rft_panel, model_cls=BloodResultsRft).fieldsets


# from django.contrib import admin
# from edc_model_admin import audit_fieldset_tuple
#
# from ...admin_site import meta_subject_admin
# from ...forms import BloodResultsRftForm
# from ...models import BloodResultsRft
# from .blood_results_modeladmin_mixin import (
#     BloodResultsModelAdminMixin,
#     conclusion_fieldset,
#     summary_fieldset,
# )
#
#
# @admin.register(BloodResultsRft, site=meta_subject_admin)
# class BloodResultsRftAdmin(BloodResultsModelAdminMixin):
#
#     form = BloodResultsRftForm
#
#     autocomplete_fields = ["rft_requisition"]
#
#     fieldsets = (
#         (None, {"fields": ("subject_visit", "report_datetime")}),
#         ("Renal Function Tests", {"fields": ["rft_requisition", "rft_assay_datetime"]}),
#         (
#             "Serum Urea",
#             {
#                 "fields": [
#                     "urea_value",
#                     "urea_units",
#                     "urea_abnormal",
#                     "urea_reportable",
#                 ]
#             },
#         ),
#         (
#             "Serum Creatinine",
#             {
#                 "fields": [
#                     "creatinine_value",
#                     "creatinine_units",
#                     "creatinine_abnormal",
#                     "creatinine_reportable",
#                 ]
#             },
#         ),
#         (
#             "Serum Uric Acid",
#             {
#                 "fields": [
#                     "uric_acid_value",
#                     "uric_acid_units",
#                     "uric_acid_abnormal",
#                     "uric_acid_reportable",
#                 ]
#             },
#         ),
#         ("eGFR (Calculated)", {"fields": ["egfr_value"]}),
#         conclusion_fieldset,
#         summary_fieldset,
#         audit_fieldset_tuple,
#     )
#
#     readonly_fields = ["egfr_value"]
