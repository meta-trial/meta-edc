from clinicedc_constants import NO, OTHER, YES


class ArvHistoryFormValidatorMixin:
    def validate_arv_history_fields(self):
        self.date_not_before(
            "arv_initiation_date",
            "viral_load_date",
            "Invalid. Cannot be before ARV initiation date.",
        )

        self.date_not_before(
            "arv_initiation_date",
            "current_arv_regimen_date",
            "Invalid. Cannot be before ARV initiation date.",
        )

        self.required_if_not_none(
            "viral_load", "viral_load_date", field_required_evaluate_as_int=True
        )

        self.date_not_before(
            "hiv_diagnosis_date",
            "viral_load_date",
            "Invalid. Cannot be before HIV diagnosis date.",
        )

        self.required_if_not_none("cd4", "cd4_date", field_required_evaluate_as_int=True)

        self.date_not_before(
            "hiv_diagnosis_date",
            "cd4_date",
            "Invalid. Cannot be before HIV diagnosis date.",
        )

        self.required_if(
            OTHER,
            field="current_arv_regimen",
            field_required="other_current_arv_regimen",
        )

        self.required_if(
            YES, field="has_previous_arv_regimen", field_required="previous_arv_regimen"
        )

        if self.cleaned_data.get("has_previous_arv_regimen") == NO:
            self.date_equal(
                "arv_initiation_date",
                "current_arv_regimen_start_date",
                "Invalid. Expected current regimen date to equal initiation date.",
            )

        self.required_if(
            YES, field="has_previous_arv_regimen", field_required="previous_arv_regimen"
        )

        self.required_if(
            OTHER,
            field="previous_arv_regimen",
            field_required="other_previous_arv_regimen",
        )

        self.required_if(YES, field="on_oi_prophylaxis", field_required="oi_prophylaxis")

        self.m2m_other_specify(
            OTHER, m2m_field="oi_prophylaxis", field_other="other_oi_prophylaxis"
        )
