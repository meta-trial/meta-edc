from edc_reportable.form_validator_mixin import ReportablesFormValidatorMixin
from edc_lab.form_validators import CrfRequisitionFormValidatorMixin
from edc_form_validators.form_validator import FormValidator
from edc_reportable.constants import GRADE3, GRADE4
from edc_constants.constants import YES


class BloodResultsFormValidatorMixin(
    ReportablesFormValidatorMixin, CrfRequisitionFormValidatorMixin, FormValidator
):

    reportable_grades = [GRADE3, GRADE4]
    reference_list_name = "meta"
    requisition_field = None
    assay_datetime_field = None
    field_names = []
    panels = []
    poc_panels = []

    @property
    def field_values(self):
        return [
            self.cleaned_data.get(f) is not None for f in [f for f in self.field_names]
        ]

    @property
    def extra_options(self):
        return {}

    def clean(self):
        self.required_if_true(
            any(self.field_values), field_required=self.requisition_field
        )

        if self.cleaned_data.get("is_poc") and self.cleaned_data.get("is_poc") == YES:
            self.validate_requisition(
                self.requisition_field, self.assay_datetime_field, *self.poc_panels
            )
        else:
            self.validate_requisition(
                self.requisition_field, self.assay_datetime_field, *self.panels
            )

        for field_name in self.field_names:
            if f"{field_name}_units" in self.cleaned_data:
                self.required_if_not_none(
                    field=field_name,
                    field_required=f"{field_name}_units",
                    field_required_evaluate_as_int=True,
                )
            if f"{field_name}_abnormal" in self.cleaned_data:
                self.required_if_not_none(
                    field=field_name,
                    field_required=f"{field_name}_abnormal",
                    field_required_evaluate_as_int=True,
                )
            if f"{field_name}_reportable" in self.cleaned_data:
                self.required_if_not_none(
                    field=field_name,
                    field_required=f"{field_name}_reportable",
                    field_required_evaluate_as_int=True,
                )

        self.validate_reportable_fields(
            reference_list_name=self.reference_list_name, **self.extra_options
        )
