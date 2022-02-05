from edc_reportable import (
    MICROMOLES_PER_LITER,
    MILLIMOLES_PER_LITER,
    ConversionNotHandled,
    calculate_bmi,
    calculate_egfr,
    convert_units,
)
from edc_screening.screening_eligibility import FC, ScreeningEligibility


class BaseEligibilityPartThree(ScreeningEligibility):
    eligible_fld_name = "eligible_part_three"
    reasons_ineligible_fld_name = "reasons_ineligible_part_three"

    def __init__(self, **kwargs):
        self.bmi = None
        self.calculated_egfr_value = None
        self.converted_creatinine_value = None
        self.converted_ifg_value = None
        self.converted_ogtt_value = None
        self.creatinine_units = None
        self.creatinine_value = None
        # self.eligible_part_three = None
        self.height = None
        self.ifg_units = None
        self.ifg_value = None
        self.ogtt_units = None
        self.ogtt_value = None
        self.weight = None
        super().__init__(**kwargs)

    def assess_eligibility(self) -> None:
        self.convert_lab_values_to_standard_units()
        self.bmi = calculate_bmi(weight_kg=self.weight, height_cm=self.height)
        self.calculated_egfr_value = calculate_egfr(**self.model_obj.__dict__)

    def set_fld_attrs_on_model(self) -> None:
        self.model_obj.converted_creatinine_value = self.converted_creatinine_value
        self.model_obj.converted_ifg_value = self.converted_ifg_value
        self.model_obj.converted_ogtt_value = self.converted_ogtt_value
        if self.bmi:
            self.model_obj.calculated_bmi_value = self.bmi.value

    def get_required_fields(self) -> dict[str, FC]:
        return {
            "creatinine_units": FC(ignore_if_missing=True),
            "creatinine_value": FC(ignore_if_missing=True),
            "height": FC(value=range(0, 500), msg="Missing height"),
            "ifg_units": FC(ignore_if_missing=True),
            "ifg_value": FC(ignore_if_missing=True),
            "ogtt_units": FC(ignore_if_missing=True),
            "ogtt_value": FC(ignore_if_missing=True),
            "weight": FC(value=range(0, 500), msg="Missing weight"),
        }

    def convert_lab_values_to_standard_units(self) -> None:
        try:
            self.converted_creatinine_value = convert_units(
                self.creatinine_value,
                units_from=self.creatinine_units,
                units_to=MICROMOLES_PER_LITER,
            )
        except ConversionNotHandled as e:
            raise ConversionNotHandled(f"Creatinine. {e}")
        try:
            self.converted_ifg_value = convert_units(
                self.ifg_value,
                units_from=self.ifg_units,
                units_to=MILLIMOLES_PER_LITER,
            )
        except ConversionNotHandled as e:
            raise ConversionNotHandled(f"IFG. {e}")
        try:
            self.converted_ogtt_value = convert_units(
                self.ogtt_value,
                units_from=self.ogtt_units,
                units_to=MILLIMOLES_PER_LITER,
            )
        except ConversionNotHandled as e:
            raise ConversionNotHandled(f"OGTT. {e}")
