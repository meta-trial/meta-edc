"""Michigan Neuropathy Screening Instrument (MNSI) calculators."""
from edc_constants.constants import ABSENT, NO, PRESENT, YES

from meta_subject.constants import DECREASED, PRESENT_REINFORCEMENT, REDUCED


class MnsiPatientHistoryCalculatorError(Exception):
    pass


class MnsiPhysicalAssessmentCalculatorError(Exception):
    pass


class MnsiCalculator:
    def __init__(self, model_obj=None, **kwargs):
        if model_obj:
            self.responses = model_obj.__dict__
        else:
            self.responses = kwargs

    def __repr__(self):
        return f"{self.__class__.__name__}(responses={self.responses})"

    def __str__(self):
        return f"{self.__class__.__name__}(responses={self.responses})"

    def patient_history_score(self) -> int:
        """Returns MSNI score based on patient history questionnaire.

        Scoring based on:
            https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3641573/#S6title
        """
        try:
            # 1 point added for each 'YES' response for following Qs
            score = [
                self.responses["numb_legs_feet"],  # Q1
                self.responses["burning_pain_legs_feet"],  # Q2
                self.responses["feet_sensitive_touch"],  # Q3
                self.responses["prickling_feelings_legs_feet"],  # Q5
                self.responses["covers_touch_skin_painful"],  # Q6
                self.responses["open_sore_foot_history"],  # Q8
                self.responses["diabetic_neuropathy"],  # Q9
                self.responses["symptoms_worse_night"],  # Q11
                self.responses["legs_hurt_when_walk"],  # Q12
                self.responses["skin_cracks_open_feet"],  # Q14
                self.responses["amputation"],  # Q15
            ].count(YES)

            # 1 point added for each 'NO' response for following Qs
            score += [
                self.responses["differentiate_hot_cold_water"],  # Q7
                self.responses["sense_feet_when_walk"],  # Q13
            ].count(NO)

            # Note: Questions 4 (muscle_cramps_legs_feet) and 10 (feel_weak)
            # not included in scoring algorithm

        except KeyError as exc:
            raise MnsiPatientHistoryCalculatorError(
                f"Can't calculate patient history score for MNSI. "
                f"Expected response '{exc.args[0]}' "
                f"was missing from received responses: {self.responses.keys()}. "
                "Perhaps catch this in the form validation."
            )
        return score

    def physical_assessment_score(self) -> float:
        """Returns score based on lower extremity examination.

        Scoring based on:
            https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3641573/#S6title
            (plus up to 2 extra points awarded for monofilament assessments)
        """
        try:
            score = float(self._get_appearance_points())
            score += self._get_ulceration_points()
            score += self._get_ankle_reflex_points()
            score += self._get_vibration_perception_points()
            score += self._get_monofilament_points()

        except KeyError as exc:
            raise MnsiPhysicalAssessmentCalculatorError(
                f"Can't calculate physical assessment score for MNSI. "
                f"Expected response '{exc.args[0]}' "
                f"was missing from received responses: {self.responses.keys()}. "
                "Perhaps catch this in the form validation."
            )

        return score

    def _get_appearance_points(self) -> int:
        return [
            self.responses["normal_appearance_right_foot"],
            self.responses["normal_appearance_left_foot"],
        ].count(NO)

    def _get_ulceration_points(self) -> int:
        return [
            self.responses["ulceration_right_foot"],
            self.responses["ulceration_left_foot"],
        ].count(PRESENT)

    def _get_ankle_reflex_points(self) -> float:
        score = 0.0
        for assessment in [
            self.responses["ankle_reflexes_right_foot"],
            self.responses["ankle_reflexes_left_foot"],
        ]:
            if assessment == PRESENT_REINFORCEMENT:
                score += 0.5
            elif assessment == ABSENT:
                score += 1.0
        return score

    def _get_vibration_perception_points(self) -> float:
        score = 0.0
        for assessment in [
            self.responses["vibration_perception_right_toe"],
            self.responses["vibration_perception_left_toe"],
        ]:
            if assessment == DECREASED:
                score += 0.5
            elif assessment == ABSENT:
                score += 1.0
        return score

    def _get_monofilament_points(self) -> float:
        score = 0.0
        for assessment in [
            self.responses["monofilament_right_foot"],
            self.responses["monofilament_left_foot"],
        ]:
            if assessment == REDUCED:
                score += 0.5
            elif assessment == ABSENT:
                score += 1.0
        return score
