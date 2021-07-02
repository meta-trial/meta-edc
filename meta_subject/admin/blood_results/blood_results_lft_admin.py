from django.contrib import admin
from edc_blood_results.admin import BloodResultsModelAdminMixin
from edc_blood_results.fieldsets import BloodResultFieldset
from edc_lab_panel.panels import lft_panel

from ...admin_site import meta_subject_admin
from ...forms import BloodResultsLftForm
from ...models import BloodResultsLft
from ..modeladmin import CrfModelAdmin


@admin.register(BloodResultsLft, site=meta_subject_admin)
class BloodResultsLftAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsLftForm
    fieldsets = BloodResultFieldset(lft_panel, model_cls=BloodResultsLft).fieldsets


# from django.contrib import admin
# from edc_blood_results.admin import BloodResultsModelAdminMixin
# from edc_model_admin import audit_fieldset_tuple
#
# from ...admin_site import meta_subject_admin
# from ...forms import BloodResultsLftForm
# from ...models import BloodResultsLft
#
#
# @admin.register(BloodResultsLft, site=meta_subject_admin)
# class BloodResultsLftAdmin(BloodResultsModelAdminMixin):
#
#     form = BloodResultsLftForm
#
#     autocomplete_fields = ["lft_requisition"]
#
#     fieldsets = (
#         (None, {"fields": ("subject_visit", "report_datetime")}),
#         ("Liver Function Tests", {"fields": ["lft_requisition", "lft_assay_datetime"]}),
#         (
#             "AST",
#             {"fields": ["ast_value", "ast_units", "ast_abnormal", "ast_reportable"]},
#         ),
#         (
#             "ALT",
#             {"fields": ["alt_value", "alt_units", "alt_abnormal", "alt_reportable"]},
#         ),
#         (
#             "ALP",
#             {"fields": ["alp_value", "alp_units", "alp_abnormal", "alp_reportable"]},
#         ),
#         (
#             "Serum Amylase",
#             {
#                 "fields": [
#                     "amylase_value",
#                     "amylase_units",
#                     "amylase_abnormal",
#                     "amylase_reportable",
#                 ]
#             },
#         ),
#         (
#             "GGT",
#             {"fields": ["ggt_value", "ggt_units", "ggt_abnormal", "ggt_reportable"]},
#         ),
#         (
#             "Serum Albumin",
#             {
#                 "fields": [
#                     "albumin_value",
#                     "albumin_units",
#                     "albumin_abnormal",
#                     "albumin_reportable",
#                 ]
#             },
#         ),
#         conclusion_fieldset,
#         summary_fieldset,
#         audit_fieldset_tuple,
#     )
