from clinicedc_constants import CLOSED, OTHER, YES
from edc_form_validators import FormValidator
from edc_prn.modelform_mixins import PrnFormValidatorMixin


class ProtocolIncidentFormValidator(PrnFormValidatorMixin, FormValidator):
    def clean(self):
        self.required_if(YES, field="safety_impact", field_required="safety_impact_details")

        self.required_if(
            YES,
            field="study_outcomes_impact",
            field_required="study_outcomes_impact_details",
        )

        self.validate_other_specify(
            field="violation_type",
            other_specify_field="violation_type_other",
            other_stored_value=OTHER,
        )

        self.required_if_not_none(
            field="corrective_action_datetime", field_required="corrective_action"
        )

        self.required_if_not_none(
            field="preventative_action_datetime", field_required="preventative_action"
        )

        self.required_if(
            CLOSED, field="report_status", field_required="report_closed_datetime"
        )
