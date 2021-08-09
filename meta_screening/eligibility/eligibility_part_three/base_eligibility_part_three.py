from edc_constants.constants import TBD
from edc_reportable import (
    MICROMOLES_PER_LITER,
    MILLIMOLES_PER_LITER,
    ConversionNotHandled,
    calculate_bmi,
    convert_units,
)

from ..base_eligibility_part_x import BaseEligibilityPartX


class BaseEligibilityPartThree(BaseEligibilityPartX):
    def assess_eligibility(self):
        # TODO: check if calculates correctly if glucose is HIGH 9999.99
        self.obj.eligible_part_three = TBD
        self.obj.reasons_ineligible_part_three = None
        self.convert_lab_values_to_standard_units()
        bmi = calculate_bmi(weight_kg=self.obj.weight, height_cm=self.obj.height)
        if bmi:
            self.obj.calculated_bmi_value = bmi.value

    @classmethod
    def get_required_fields(cls):
        return None

    def get_reasons_ineligible(self, *args):
        return None

    def convert_lab_values_to_standard_units(self):
        try:
            self.obj.converted_creatinine_value = convert_units(
                self.obj.creatinine_value,
                units_from=self.obj.creatinine_units,
                units_to=MICROMOLES_PER_LITER,
            )
        except ConversionNotHandled as e:
            raise ConversionNotHandled(f"Creatinine. {e}")
        try:
            self.obj.converted_ifg_value = convert_units(
                self.obj.ifg_value,
                units_from=self.obj.ifg_units,
                units_to=MILLIMOLES_PER_LITER,
            )
        except ConversionNotHandled as e:
            raise ConversionNotHandled(f"IFG. {e}")
        try:
            self.obj.converted_ogtt_value = convert_units(
                self.obj.ogtt_value,
                units_from=self.obj.ogtt_units,
                units_to=MILLIMOLES_PER_LITER,
            )
        except ConversionNotHandled as e:
            raise ConversionNotHandled(f"OGTT. {e}")
