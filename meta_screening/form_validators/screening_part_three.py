from django import forms
from edc_constants.constants import NEG, NO, POS, YES
from edc_form_validators import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin
from edc_glucose.utils import validate_glucose_as_millimoles_per_liter
from edc_reportable import BmiFormValidatorMixin, EgfrFormValidatorMixin
from edc_vitals.form_validators import (
    BloodPressureFormValidatorMixin,
    WeightHeightBmiFormValidatorMixin,
)

from meta_edc.meta_version import PHASE_THREE, PHASE_TWO, get_meta_version
from meta_screening.forms import get_part_three_vitals_fields


class ScreeningPartThreeFormValidatorError(Exception):
    pass


class ScreeningPartThreeFormValidator(
    GlucoseFormValidatorMixin,
    BmiFormValidatorMixin,
    EgfrFormValidatorMixin,
    BloodPressureFormValidatorMixin,
    WeightHeightBmiFormValidatorMixin,
    FormValidator,
):
    def clean(self):
        if get_meta_version() == PHASE_TWO:
            self.clean_phase_two()
        elif get_meta_version() == PHASE_THREE:
            self.clean_phase_three()

    def clean_phase_two(self):
        self.validate_report_datetimes()
        self.validate_ifg_required_fields()
        validate_glucose_as_millimoles_per_liter("ifg", self.cleaned_data)
        self.validate_ogtt_required_fields()
        validate_glucose_as_millimoles_per_liter("ogtt", self.cleaned_data)
        self.validate_creatinine_required_fields()
        self.required_if(YES, field="hba1c_performed", field_required="hba1c_value")
        self.require_all_vitals_fields()
        self.validate_pregnancy()
        self.validate_ogtt_dates()
        self.validate_bmi()
        self.validate_egfr()
        self.validate_ifg_before_ogtt()
        self.validate_ogtt_time_interval()
        self.validate_suitability_for_study()

    def clean_phase_three(self):
        self.validate_report_datetimes()
        self.require_all_vitals_fields()
        self.validate_weight_height_with_bmi(
            weight_kg=self.cleaned_data.get("weight"),
            height_cm=self.cleaned_data.get("height"),
        )
        self.raise_on_avg_blood_pressure_suggests_severe_htn(**self.cleaned_data)
        self.validate_pregnancy()
        self.validate_ifg_required_fields()
        validate_glucose_as_millimoles_per_liter("ifg", self.cleaned_data)
        self.validate_ifg_before_ogtt()
        self.validate_ogtt_time_interval()
        self.validate_ogtt_required_fields()
        self.validate_ogtt_dates()
        validate_glucose_as_millimoles_per_liter("ogtt", self.cleaned_data)
        self.validate_creatinine_required_fields()
        self.required_if(YES, field="hba1c_performed", field_required="hba1c_value")
        self.validate_egfr()
        self.validate_suitability_for_study()

    def validate_report_datetimes(self):
        pass
        # report_datetime = self.self.cleaned_data.get("report_datetime")
        # part_two_report_datetime = self.self.cleaned_data.get(
        #     "part_two_report_datetime"
        # )
        # part_three_report_datetime = self.self.cleaned_data.get(
        #     "part_three_report_datetime"
        # )
        # if part_two_report_datetime < report_datetime:
        #     raise forms.ValidationError()

    def validate_suitability_for_study(self):
        self.required_if(
            YES, field="unsuitable_for_study", field_required="reasons_unsuitable"
        )

        self.applicable_if(
            YES, field="unsuitable_for_study", field_applicable="unsuitable_agreed"
        )

        if self.cleaned_data.get("unsuitable_agreed") == NO:
            raise forms.ValidationError(
                {
                    "unsuitable_agreed": "The study coordinator MUST agree "
                    "with your assessment. Please discuss before continuing."
                }
            )

    def validate_creatinine_required_fields(self):
        self.required_if(
            YES, field="creatinine_performed", field_required="creatinine_value"
        )
        self.required_if_true(
            self.cleaned_data.get("creatinine_value"), field_required="creatinine_units"
        )

    def validate_pregnancy(self):
        self.applicable_if(
            YES,
            NO,
            field="pregnant",
            field_applicable="urine_bhcg_performed",
            is_instance_field=True,
            msg="See response in part one.",
        )
        self.applicable_if(
            YES, field="urine_bhcg_performed", field_applicable="urine_bhcg_value"
        )
        self.required_if(
            YES, field="urine_bhcg_performed", field_required="urine_bhcg_date"
        )

        if (
            self.instance.pregnant == YES
            and self.cleaned_data.get("urine_bhcg_value") == NEG
        ):
            raise forms.ValidationError(
                {"urine_bhcg_value": "Invalid, part one says subject is pregnant"}
            )
        elif (
            self.instance.pregnant == NO
            and self.cleaned_data.get("urine_bhcg_value") == POS
        ):
            raise forms.ValidationError(
                {"urine_bhcg_value": "Invalid, part one says subject is not pregnant"}
            )

    def require_all_vitals_fields(self):
        require_all = False
        fields = get_part_three_vitals_fields()
        for field in fields:
            if self.cleaned_data.get(field):
                require_all = True
                break
        if require_all:
            for field in fields:
                if not self.cleaned_data.get(field):
                    raise forms.ValidationError({field: "This field is required"})
