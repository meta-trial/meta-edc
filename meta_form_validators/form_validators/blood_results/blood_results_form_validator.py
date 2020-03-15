from django import forms
from meta_labs.panels import (
    blood_glucose_panel,
    blood_glucose_poc_panel,
    chemistry_panel,
    fbc_panel,
    hba1c_panel,
    hba1c_poc_panel,
)
from edc_constants.constants import FASTING

from .blood_results_form_validator_mixin import BloodResultsFormValidatorMixin


class BloodResultsGluFormValidator(BloodResultsFormValidatorMixin):

    requisition_field = "glucose_requisition"
    assay_datetime_field = "glucose_assay_datetime"
    field_names = ["glucose", "fasting"]
    panels = [blood_glucose_panel]
    poc_panels = [blood_glucose_poc_panel]

    @property
    def extra_options(self):
        if not self.cleaned_data.get("fasting"):
            raise forms.ValidationError({"fasting": "This field is required."})
        fasting = True if self.cleaned_data.get("fasting") == FASTING else False
        return dict(fasting=fasting)


class BloodResultsFbcFormValidator(BloodResultsFormValidatorMixin):

    requisition_field = "fbc_requisition"
    assay_datetime_field = "fbc_assay_datetime"
    field_names = ["haemoglobin", "hct", "rbc", "wbc", "platelets"]
    panels = [fbc_panel]


class BloodResultsHba1cFormValidator(BloodResultsFormValidatorMixin):

    requisition_field = "hba1c_requisition"
    assay_datetime_field = "hba1c_assay_datetime"
    field_names = ["hba1c"]
    panels = [hba1c_panel]
    poc_panels = [hba1c_poc_panel]

    def validate_reportable_fields(self, **kwargs):
        pass


class BloodResultsLipidFormValidator(BloodResultsFormValidatorMixin):

    requisition_field = "lipid_requisition"
    assay_datetime_field = "lipid_assay_datetime"
    field_names = ["ldl", "hdl", "trig"]
    panels = [chemistry_panel]


class BloodResultsLftFormValidator(BloodResultsFormValidatorMixin):

    requisition_field = "lft_requisition"
    assay_datetime_field = "lft_assay_datetime"
    field_names = ["ast", "alt", "alp", "amylase", "ggt", "albumin"]
    panels = [chemistry_panel]


class BloodResultsRftFormValidator(BloodResultsFormValidatorMixin):

    requisition_field = "rft_requisition"
    assay_datetime_field = "rft_assay_datetime"
    field_names = ["urea", "creatinine", "uric_acid", "egfr"]
    panels = [chemistry_panel]
