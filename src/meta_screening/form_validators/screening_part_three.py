from __future__ import annotations

from datetime import datetime

from clinicedc_constants import NO, YES
from django import forms
from edc_egfr.form_validator_mixins import EgfrCkdEpiFormValidatorMixin
from edc_form_validators import INVALID_ERROR, FormValidator
from edc_glucose.form_validators import (
    FastingFormValidatorMixin,
    FbgOgttFormValidatorMixin,
)
from edc_glucose.utils import validate_glucose_as_millimoles_per_liter
from edc_prn.modelform_mixins import PrnFormValidatorMixin
from edc_utils import formatted_datetime
from edc_utils.date import to_local, to_utc
from edc_vitals.form_validators import (
    BloodPressureFormValidatorMixin,
    WeightHeightBmiFormValidatorMixin,
)

from ..forms import part_three_vitals_fields
from ..models import SubjectScreening


class ScreeningPartThreeFormValidatorError(Exception):
    pass


class ScreeningPartThreeFormValidator(
    FastingFormValidatorMixin,
    FbgOgttFormValidatorMixin,
    EgfrCkdEpiFormValidatorMixin,
    BloodPressureFormValidatorMixin,
    WeightHeightBmiFormValidatorMixin,
    PrnFormValidatorMixin,
    FormValidator,
):
    report_datetime_field_attr = "part_three_report_datetime"

    def clean(self):
        self.validate_report_datetimes()
        self.require_all_vitals_fields()
        self.validate_weight_height_with_bmi(
            weight_kg=self.cleaned_data.get("weight"),
            height_cm=self.cleaned_data.get("height"),
            lower_bmi_value=SubjectScreening.lower_bmi_value,
            upper_bmi_value=SubjectScreening.upper_bmi_value,
        )
        self.raise_on_avg_blood_pressure_suggests_severe_htn(**self.cleaned_data)
        self.validate_pregnancy()
        self.validate_fasting_required_fields()
        self.validate_fbg_required_fields("fbg")
        validate_glucose_as_millimoles_per_liter("fbg", self.cleaned_data)
        self.validate_fbg_before_ogtt()
        self.validate_ogtt_time_interval()
        self.validate_ogtt_required_fields()
        self.validate_ogtt_dates()
        validate_glucose_as_millimoles_per_liter("ogtt", self.cleaned_data)

        self.required_if(
            YES, field="repeat_glucose_opinion", field_required="repeat_appt_datetime"
        )
        self.required_if(
            YES, field="repeat_glucose_opinion", field_required="contact_number", inverse=False
        )

        self.applicable_if(
            YES, field="repeat_glucose_performed", field_applicable="repeat_fasting"
        )
        self.validate_fasting_required_fields(fasting_prefix="repeat_fasting")
        self.validate_repeat_fbg()
        self.validate_repeat_ogtt()
        self.validate_creatinine_required_fields()
        self.required_if(YES, field="hba1c_performed", field_required="hba1c_datetime")
        self.required_if(YES, field="hba1c_performed", field_required="hba1c_value")
        self.validate_egfr(
            gender=self.instance.gender,
            age_in_years=self.instance.age_in_years,
            ethnicity=self.instance.ethnicity,
        )
        self.validate_suitability_for_study()

    @property
    def part_two_report_datetime(self) -> datetime | None:
        return self.instance.part_two_report_datetime

    def validate_repeat_fbg(self):
        """Validate like first FBG and ...

        Ensure repeat FBG at least three days after first FBG
        """
        self.applicable_if(
            YES,
            field="repeat_glucose_opinion",
            field_applicable="repeat_glucose_performed",
        )
        for fld in [
            "fbg2_datetime",
            "fbg2_value",
            "fbg2_units",
        ]:
            self.required_if(YES, field="repeat_glucose_performed", field_required=fld)

    def validate_repeat_ogtt(self):
        """Validate like first OGTT and ...

        Ensure repeat OGTT at least three days after first OGTT
        """
        self.applicable_if(
            YES,
            field="repeat_glucose_opinion",
            field_applicable="repeat_glucose_performed",
        )
        for fld in [
            "ogtt2_base_datetime",
            "ogtt2_datetime",
            "ogtt2_value",
            "ogtt2_units",
        ]:
            self.required_if(YES, field="repeat_glucose_performed", field_required=fld)
        if self.cleaned_data.get("repeat_glucose_performed") == YES:
            for ogtt_dte, ogtt2_dte in [
                ("ogtt_base_datetime", "ogtt2_base_datetime"),
                ("ogtt_datetime", "ogtt2_datetime"),
            ]:
                if self.cleaned_data.get(ogtt_dte) and self.cleaned_data.get(ogtt2_dte):
                    tdelta = (
                        self.cleaned_data.get(ogtt2_dte).date()
                        - self.cleaned_data.get(ogtt_dte).date()
                    )
                    if tdelta.days < 3:
                        raise forms.ValidationError(
                            {ogtt2_dte: "Invalid. Must be at least 3 days after first OGTT"}
                        )
            self.validate_ogtt_time_interval(ogtt_prefix="ogtt2")
            self.validate_ogtt_required_fields(ogtt_prefix="ogtt2")
            self.validate_ogtt_dates(ogtt_prefix="ogtt2")
            validate_glucose_as_millimoles_per_liter("ogtt2", self.cleaned_data)

    def validate_report_datetimes(self):
        if (
            self.report_datetime
            and self.part_two_report_datetime
            and to_utc(self.report_datetime) < self.part_two_report_datetime
        ):
            dte = formatted_datetime(to_local(self.part_two_report_datetime))
            self.raise_validation_error(
                {
                    self.report_datetime_field_attr: (
                        "Cannot be before Part Two report datetime. "
                        f"Expected date after {dte}."
                    )
                },
                INVALID_ERROR,
            )

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
        self.required_if(YES, field="creatinine_performed", field_required="creatinine_value")
        self.required_if_true(
            self.cleaned_data.get("creatinine_value"), field_required="creatinine_units"
        )

    def validate_pregnancy(self):
        # TODO: REVIEW FOR INVALID PERMUTATIONS SNK3BYP7 (AMANA)
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
        self.required_if(YES, field="urine_bhcg_performed", field_required="urine_bhcg_date")

    def require_all_vitals_fields(self):
        require_all = False
        fields = part_three_vitals_fields
        for field in fields:
            if self.cleaned_data.get(field):
                require_all = True
                break
        if require_all:
            for field in fields:
                if not self.cleaned_data.get(field):
                    raise forms.ValidationError({field: "This field is required"})
