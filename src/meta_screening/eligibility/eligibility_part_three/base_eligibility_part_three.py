import contextlib

from clinicedc_constants import (
    MICROMOLES_PER_LITER,
    MILLIMOLES_PER_LITER,
    NEG,
    NO,
    NOT_APPLICABLE,
)
from clinicedc_utils import (
    ConversionNotHandled,
    EgfrCalculatorError,
    EgfrCkdEpi2009,
    convert_units,
)
from edc_screening.fc import FC
from edc_screening.screening_eligibility import ScreeningEligibility
from edc_vitals.calculators import calculate_bmi


class BaseEligibilityPartThree(ScreeningEligibility):
    eligible_fld_name = "eligible_part_three"
    reasons_ineligible_fld_name = "reasons_ineligible_part_three"

    def __init__(self, **kwargs):
        self.bmi = None
        self.calculated_egfr_value = None
        self.creatinine_units = None
        self.creatinine_value = None
        self.height = None
        self.fbg_units = None
        self.fbg2_units = None
        self.fbg_value = None
        self.fbg2_value = None
        self.ogtt_units = None
        self.ogtt_value = None
        self.ogtt2_units = None
        self.ogtt2_value = None
        self.repeat_glucose_opinion = None
        self.repeat_glucose_performed = None
        self.weight = None
        self.unsuitable_agreed = None
        self.urine_bhcg_value = None
        super().__init__(**kwargs)

    def assess_eligibility(self) -> None:
        if self.weight and self.height:
            self.bmi = calculate_bmi(weight_kg=self.weight, height_cm=self.height)
        with contextlib.suppress(EgfrCalculatorError):
            self.calculated_egfr_value = EgfrCkdEpi2009(
                gender=self.model_obj.gender,
                age_in_years=self.model_obj.age_in_years,
                ethnicity=self.model_obj.gender,
                creatinine_value=self.model_obj.creatinine_value,
                creatinine_units=self.model_obj.creatinine_units,
            ).value

    def set_fld_attrs_on_model(self) -> None:
        self.model_obj.converted_creatinine_value = self.converted_creatinine_value
        self.model_obj.converted_fbg_value = self.converted_fbg_value
        self.model_obj.converted_ogtt_value = self.converted_ogtt_value
        self.model_obj.converted_fbg2_value = self.converted_fbg2_value
        self.model_obj.converted_ogtt2_value = self.converted_ogtt2_value
        if self.bmi:
            self.model_obj.calculated_bmi_value = self.bmi.value

    def get_required_fields(self) -> dict[str, FC]:
        return {
            "creatinine_units": FC(ignore_if_missing=True),
            "creatinine_value": FC(ignore_if_missing=True),
            "height": FC(value=range(0, 500), msg="Missing height"),
            "fbg_units": FC(ignore_if_missing=True),
            "fbg2_units": FC(ignore_if_missing=True),
            "fbg_value": FC(ignore_if_missing=True),
            "fbg2_value": FC(ignore_if_missing=True),
            "ogtt_units": FC(ignore_if_missing=True),
            "ogtt_value": FC(ignore_if_missing=True),
            "ogtt2_units": FC(ignore_if_missing=True),
            "ogtt2_value": FC(ignore_if_missing=True),
            "weight": FC(value=range(0, 500), msg="Missing weight"),
            "repeat_glucose_opinion": FC(ignore_if_missing=True),
            "repeat_glucose_performed": FC(ignore_if_missing=True),
            "urine_bhcg_value": FC(value=[NEG, NOT_APPLICABLE], msg="UPT positive"),
            "unsuitable_agreed": FC(value=[NO, NOT_APPLICABLE]),
        }

    @property
    def converted_creatinine_value(self):
        value = None
        if self.creatinine_value and self.creatinine_units:
            try:
                value = convert_units(
                    label="creatinine",
                    value=self.creatinine_value,
                    units_from=self.creatinine_units,
                    units_to=MICROMOLES_PER_LITER,
                )
            except ConversionNotHandled as e:
                raise ConversionNotHandled(f"Creatinine. {e}") from e
        if value and float(value) > 999999.9999:
            raise ConversionNotHandled("Creatinine value is absurd.")
        return value

    @property
    def converted_fbg_value(self):
        value = None
        if self.fbg_value and self.fbg_units:
            try:
                value = convert_units(
                    label="glucose",
                    value=self.fbg_value,
                    units_from=self.fbg_units,
                    units_to=MILLIMOLES_PER_LITER,
                )
            except ConversionNotHandled as e:
                raise ConversionNotHandled(f"FBG. {e}") from e
        return value

    @property
    def converted_fbg2_value(self):
        value = None
        if self.fbg2_value and self.fbg2_units:
            try:
                value = convert_units(
                    label="glucose",
                    value=self.fbg2_value,
                    units_from=self.fbg2_units,
                    units_to=MILLIMOLES_PER_LITER,
                )
            except ConversionNotHandled as e:
                raise ConversionNotHandled(f"FBG2. {e}") from e
        return value

    @property
    def converted_ogtt_value(self):
        value = None
        if self.ogtt_value and self.ogtt_units:
            try:
                value = convert_units(
                    label="glucose",
                    value=self.ogtt_value,
                    units_from=self.ogtt_units,
                    units_to=MILLIMOLES_PER_LITER,
                )
            except ConversionNotHandled as e:
                raise ConversionNotHandled(f"OGTT. {e}") from e
        return value

    @property
    def converted_ogtt2_value(self):
        value = None
        if self.ogtt2_value and self.ogtt2_units:
            try:
                value = convert_units(
                    label="glucose",
                    value=self.ogtt2_value,
                    units_from=self.ogtt2_units,
                    units_to=MILLIMOLES_PER_LITER,
                )
            except ConversionNotHandled as e:
                raise ConversionNotHandled(f"OGTT2. {e}") from e
        return value

    def set_eligible_model_field(self):
        setattr(self.model_obj, self.eligible_fld_name, self.eligible)
