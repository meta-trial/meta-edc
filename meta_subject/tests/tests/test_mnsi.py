from copy import deepcopy
from typing import Dict

from django.test import TestCase, override_settings
from edc_constants.constants import (
    ABSENT,
    COMPLETE,
    NO,
    NORMAL,
    NOT_APPLICABLE,
    OTHER,
    PRESENT,
    YES,
)
from edc_form_validators import FormValidatorTestCaseMixin

from meta_edc.meta_version import PHASE_THREE
from meta_lists.models import AbnormalFootAppearanceObservations
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.constants import DECREASED, PRESENT_REINFORCEMENT, REDUCED
from meta_subject.forms.mnsi_form import MnsiForm, MnsiFormValidator
from meta_subject.mnsi_calculator import (
    MnsiCalculator,
    MnsiPatientHistoryCalculatorError,
    MnsiPhysicalAssessmentCalculatorError,
)
from meta_subject.models import Mnsi


@override_settings(META_PHASE=PHASE_THREE)
class TestMnsiCalculators(MetaTestCaseMixin, TestCase):
    @staticmethod
    def get_best_case_answers():
        return {
            "mnsi_performed": YES,
            # Part 1: Patient History
            "numb_legs_feet": NO,
            "burning_pain_legs_feet": NO,
            "feet_sensitive_touch": NO,
            "muscle_cramps_legs_feet": NO,  # no effect on score, regardless of value
            "prickling_feelings_legs_feet": NO,
            "covers_touch_skin_painful": NO,
            "differentiate_hot_cold_water": YES,
            "open_sore_foot_history": NO,
            "diabetic_neuropathy": NO,
            "feel_weak": NO,  # no effect on score, regardless of value
            "symptoms_worse_night": NO,
            "legs_hurt_when_walk": NO,
            "sense_feet_when_walk": YES,
            "skin_cracks_open_feet": NO,
            "amputation": NO,
            # Part 2a: Physical Assessment - Right Foot
            "examined_right_foot": YES,
            "normal_appearance_right_foot": YES,
            "ulceration_right_foot": ABSENT,
            "ankle_reflexes_right_foot": PRESENT,
            "vibration_perception_right_toe": PRESENT,
            "monofilament_right_foot": NORMAL,
            # Part 2b: Physical Assessment - Left Foot
            "examined_left_foot": YES,
            "normal_appearance_left_foot": YES,
            "ulceration_left_foot": ABSENT,
            "ankle_reflexes_left_foot": PRESENT,
            "vibration_perception_left_toe": PRESENT,
            "monofilament_left_foot": NORMAL,
        }

    @staticmethod
    def get_worst_case_patient_history_data():
        return {
            # Part 1: Patient History
            "numb_legs_feet": YES,
            "burning_pain_legs_feet": YES,
            "feet_sensitive_touch": YES,
            "prickling_feelings_legs_feet": YES,
            "covers_touch_skin_painful": YES,
            "differentiate_hot_cold_water": NO,
            "open_sore_foot_history": YES,
            "diabetic_neuropathy": YES,
            "symptoms_worse_night": YES,
            "legs_hurt_when_walk": YES,
            "sense_feet_when_walk": NO,
            "skin_cracks_open_feet": YES,
            "amputation": YES,
        }

    @staticmethod
    def get_worst_case_physical_assessment_data():
        return {
            # Part 2a: Physical Assessment - Right Foot
            "normal_appearance_right_foot": NO,
            "ulceration_right_foot": PRESENT,
            "ankle_reflexes_right_foot": ABSENT,
            "vibration_perception_right_toe": ABSENT,
            "monofilament_right_foot": ABSENT,
            # Part 2b: Physical Assessment - Left Foot
            "normal_appearance_left_foot": NO,
            "ulceration_left_foot": PRESENT,
            "ankle_reflexes_left_foot": ABSENT,
            "vibration_perception_left_toe": ABSENT,
            "monofilament_left_foot": ABSENT,
        }

    def test_calculator_returns_same_scores_for_mnsi_model_and_dict(self):
        # Test min scores for model and dict match
        responses = self.get_best_case_answers()
        model = Mnsi(**responses)
        model_mnsi_calculator = MnsiCalculator(model)
        dict_mnsi_calculator = MnsiCalculator(**responses)

        self.assertEqual(
            model_mnsi_calculator.patient_history_score(),
            dict_mnsi_calculator.patient_history_score(),
        )
        self.assertEqual(model_mnsi_calculator.patient_history_score(), 0)
        self.assertEqual(
            model_mnsi_calculator.physical_assessment_score(),
            dict_mnsi_calculator.physical_assessment_score(),
        )
        self.assertEqual(model_mnsi_calculator.physical_assessment_score(), 0)

        # Test max scores for model and dict match
        responses.update(self.get_worst_case_patient_history_data())
        responses.update(self.get_worst_case_physical_assessment_data())
        model = Mnsi(**responses)
        model_mnsi_calculator = MnsiCalculator(model)
        dict_mnsi_calculator = MnsiCalculator(**responses)

        self.assertEqual(
            model_mnsi_calculator.patient_history_score(),
            dict_mnsi_calculator.patient_history_score(),
        )
        self.assertEqual(model_mnsi_calculator.patient_history_score(), 13)
        self.assertEqual(
            model_mnsi_calculator.physical_assessment_score(),
            dict_mnsi_calculator.physical_assessment_score(),
        )
        self.assertEqual(model_mnsi_calculator.physical_assessment_score(), 10)

    def test_missing_required_field_raises_mnsi_patient_history_calculator_error(
        self,
    ):
        responses = self.get_best_case_answers()
        responses.pop("amputation")
        mnsi_calculator = MnsiCalculator(**responses)
        with self.assertRaises(MnsiPatientHistoryCalculatorError):
            mnsi_calculator.patient_history_score()

    def test_missing_non_required_fields_does_not_raise_mnsi_patient_history_calculator_error(
        self,
    ):
        responses = self.get_best_case_answers()
        responses.pop("muscle_cramps_legs_feet")
        responses.pop("feel_weak")
        mnsi_calculator = MnsiCalculator(**responses)
        try:
            mnsi_calculator.patient_history_score()
        except MnsiPatientHistoryCalculatorError as exc:
            self.fail(
                f"mnsi_calculator.patient_history_score() raised "
                f"MnsiPatientHistoryCalculatorError unexpectedly.\nDetails: {exc}"
            )

    def test_missing_required_field_raises_mnsi_physical_assessment_calculator_error(
        self,
    ):
        responses = self.get_best_case_answers()
        responses.pop("ulceration_left_foot")
        mnsi_calculator = MnsiCalculator(**responses)
        with self.assertRaises(MnsiPhysicalAssessmentCalculatorError):
            mnsi_calculator.physical_assessment_score()

    def test_best_case_patient_history_returns_min_score_of_zero(self):
        mnsi_calculator = MnsiCalculator(**self.get_best_case_answers())
        self.assertEqual(mnsi_calculator.patient_history_score(), 0)

    def test_worst_case_patient_history_returns_max_score_of_thirteen(self):
        responses = self.get_best_case_answers()
        responses.update(self.get_worst_case_patient_history_data())
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 13)

    def test_q4_and_q10_do_not_affect_patient_history_score(self):
        # Best case score should be 0
        responses = self.get_best_case_answers()
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 0)

        # Best case score should remain 0 after modifying q4 and 10
        responses.update({"muscle_cramps_legs_feet": YES, "feel_weak": YES})
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 0)

        # Worst case score should be 13
        responses.update(self.get_worst_case_patient_history_data())
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 13)

        # Best case score should remain 13 after modifying q4 and 10
        responses.update({"muscle_cramps_legs_feet": NO, "feel_weak": NO})
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.patient_history_score(), 13)

    def test_best_case_physical_assessment_returns_min_score_of_zero(self):
        mnsi_calculator = MnsiCalculator(**self.get_best_case_answers())
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 0)

    def test_worst_case_physical_assessment_returns_max_score_of_ten(self):
        responses = self.get_best_case_answers()
        responses.update(self.get_worst_case_physical_assessment_data())
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 10)

    def test_patient_history_scores_where_YES_awards_one_point(self):
        one_point_if_yes_response_questions = [
            "numb_legs_feet",  # Q1
            "burning_pain_legs_feet",  # Q2
            "feet_sensitive_touch",  # Q3
            "prickling_feelings_legs_feet",  # Q5
            "covers_touch_skin_painful",  # Q6
            "open_sore_foot_history",  # Q8
            "diabetic_neuropathy",  # Q9
            "symptoms_worse_night",  # Q11
            "legs_hurt_when_walk",  # Q12
            "skin_cracks_open_feet",  # Q14
            "amputation",  # Q15
        ]

        for question in one_point_if_yes_response_questions:
            with self.subTest(
                f"Testing '{question}' with 'YES' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = YES
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.patient_history_score(), 1)

    def test_patient_history_scores_where_NO_awards_one_point(self):
        one_point_if_no_response_questions = [
            "differentiate_hot_cold_water",  # Q7
            "sense_feet_when_walk",  # Q13
        ]

        for question in one_point_if_no_response_questions:
            with self.subTest(
                f"Testing '{question}' with 'NO' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = NO
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.patient_history_score(), 1)

    def test_physical_assessment_abnormal_foot_appearance_awards_one_point(self):
        normal_foot_appearance_questions = [
            "normal_appearance_right_foot",
            "normal_appearance_left_foot",
        ]

        for question in normal_foot_appearance_questions:
            with self.subTest(
                f"Testing '{question}' with 'NO' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = NO
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 1.0)

    def test_physical_assessment_foot_ulceration_present_awards_one_point(self):
        ulceration_questions = [
            "ulceration_right_foot",
            "ulceration_left_foot",
        ]

        for question in ulceration_questions:
            with self.subTest(
                f"Testing '{question}' with 'PRESENT' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = PRESENT
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 1.0)

    def test_physical_assessment_ankle_reflexes_present_reinforcement_awards_half_point(
        self,
    ):
        ankle_reflex_questions = [
            "ankle_reflexes_right_foot",
            "ankle_reflexes_left_foot",
        ]

        for question in ankle_reflex_questions:
            with self.subTest(
                f"Testing '{question}' with 'PRESENT_REINFORCEMENT' response "
                "is worth 0.5 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = PRESENT_REINFORCEMENT
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 0.5)

    def test_physical_assessment_ankle_reflexes_absent_awards_one_point(
        self,
    ):
        ankle_reflex_questions = [
            "ankle_reflexes_right_foot",
            "ankle_reflexes_left_foot",
        ]

        for question in ankle_reflex_questions:
            with self.subTest(
                f"Testing '{question}' with 'ABSENT' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = ABSENT
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 1)

    def test_physical_assessment_vibration_perception_decreased_awards_half_point(
        self,
    ):
        vibration_perception_questions = [
            "vibration_perception_right_toe",
            "vibration_perception_left_toe",
        ]

        for question in vibration_perception_questions:
            with self.subTest(
                f"Testing '{question}' with 'DECREASED' response is worth 0.5 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = DECREASED
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 0.5)

    def test_physical_assessment_vibration_perception_absent_awards_one_point(
        self,
    ):
        vibration_perception_questions = [
            "vibration_perception_right_toe",
            "vibration_perception_left_toe",
        ]

        for question in vibration_perception_questions:
            with self.subTest(
                f"Testing '{question}' with 'ABSENT' response is worth 1 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = ABSENT
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 1)

    def test_physical_assessment_monofilament_reduced_awards_half_point(
        self,
    ):
        monofilament_questions = [
            "monofilament_right_foot",
            "monofilament_left_foot",
        ]

        for question in monofilament_questions:
            with self.subTest(
                f"Testing '{question}' with 'REDUCED' response is worth 0.5 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = REDUCED
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 0.5)

    def test_physical_assessment_monofilament_absent_awards_one_point(
        self,
    ):
        monofilament_questions = [
            "monofilament_right_foot",
            "monofilament_left_foot",
        ]

        for question in monofilament_questions:
            with self.subTest(
                f"Testing '{question}' with 'ABSENT' response is worth 0.5 point",
                question=question,
            ):
                responses = self.get_best_case_answers()
                responses[question] = ABSENT
                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 1)

    def test_physical_assessment_one_foot_not_examined(
        self,
    ):
        for excluded_foot in ["right", "left"]:
            with self.subTest(excluded_foot=excluded_foot):
                # Set worse case responses
                responses = self.get_best_case_answers()
                responses.update(self.get_worst_case_physical_assessment_data())

                # Set excluded foot, remove further answers
                responses[f"examined_{excluded_foot}_foot"] = NO
                responses.pop(f"normal_appearance_{excluded_foot}_foot")
                responses.pop(f"ulceration_{excluded_foot}_foot")
                responses.pop(f"ankle_reflexes_{excluded_foot}_foot")
                responses.pop(f"vibration_perception_{excluded_foot}_toe")
                responses.pop(f"monofilament_{excluded_foot}_foot")

                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 5)

    def test_physical_assessment_no_feet_examined_awards_zero_points(
        self,
    ):
        responses = self.get_best_case_answers()

        for excluded_foot in ["right", "left"]:
            # Set excluded foot, remove further answers
            responses[f"examined_{excluded_foot}_foot"] = NO
            responses.pop(f"normal_appearance_{excluded_foot}_foot")
            responses.pop(f"ulceration_{excluded_foot}_foot")
            responses.pop(f"ankle_reflexes_{excluded_foot}_foot")
            responses.pop(f"vibration_perception_{excluded_foot}_toe")
            responses.pop(f"monofilament_{excluded_foot}_foot")

        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 0)

    def test_physical_assessment_other_responses_ignored_if_foot_not_examined(
        self,
    ):
        for excluded_foot in ["right", "left"]:
            with self.subTest(excluded_foot=excluded_foot):
                # Set worse case responses
                responses = self.get_best_case_answers()
                responses.update(self.get_worst_case_physical_assessment_data())

                # Set excluded foot, don't remove further answers
                responses[f"examined_{excluded_foot}_foot"] = NO

                mnsi_calculator = MnsiCalculator(**responses)
                self.assertEqual(mnsi_calculator.physical_assessment_score(), 5)

        # Test for both feet excluded
        responses["examined_right_foot"] = NO
        responses["examined_left_foot"] = NO
        mnsi_calculator = MnsiCalculator(**responses)
        self.assertEqual(mnsi_calculator.physical_assessment_score(), 0)


@override_settings(META_PHASE=PHASE_THREE)
class TestMnsiFormValidator(MetaTestCaseMixin, FormValidatorTestCaseMixin, TestCase):

    form_validator_default_form_cls = MnsiFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_valid_form_data(self) -> Dict:
        return {
            "mnsi_performed": YES,
            "mnsi_not_performed_reason": None,
            # Part 1: Patient History
            "numb_legs_feet": NO,
            "burning_pain_legs_feet": NO,
            "feet_sensitive_touch": NO,
            "muscle_cramps_legs_feet": NO,
            "prickling_feelings_legs_feet": NO,
            "covers_touch_skin_painful": NO,
            "differentiate_hot_cold_water": YES,
            "open_sore_foot_history": NO,
            "diabetic_neuropathy": NO,
            "feel_weak": NO,
            "symptoms_worse_night": NO,
            "legs_hurt_when_walk": NO,
            "sense_feet_when_walk": YES,
            "skin_cracks_open_feet": NO,
            "amputation": NO,
            # Part 2a: Physical Assessment - Right Foot
            "examined_right_foot": YES,
            "normal_appearance_right_foot": YES,
            "ulceration_right_foot": ABSENT,
            "ankle_reflexes_right_foot": PRESENT,
            "vibration_perception_right_toe": PRESENT,
            "monofilament_right_foot": NORMAL,
            # Part 2b: Physical Assessment - Left Foot
            "examined_left_foot": YES,
            "normal_appearance_left_foot": YES,
            "ulceration_left_foot": ABSENT,
            "ankle_reflexes_left_foot": PRESENT,
            "vibration_perception_left_toe": PRESENT,
            "monofilament_left_foot": NORMAL,
            # Other
            "crf_status": COMPLETE,
            "subject_visit": self.subject_visit.pk,
            "report_datetime": self.subject_visit.report_datetime,
        }

    @staticmethod
    def get_foot_questions_with_na_answers(foot_choice: str) -> Dict[str, str]:
        return {
            f"normal_appearance_{foot_choice}_foot": NOT_APPLICABLE,
            f"ulceration_{foot_choice}_foot": NOT_APPLICABLE,
            f"ankle_reflexes_{foot_choice}_foot": NOT_APPLICABLE,
            f"vibration_perception_{foot_choice}_toe": NOT_APPLICABLE,
            f"monofilament_{foot_choice}_foot": NOT_APPLICABLE,
        }

    def test_valid_form_ok(self):
        cleaned_data = deepcopy(self.get_valid_form_data())
        form = MnsiForm(data=cleaned_data)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_physical_assessment_questions_applicable_if_foot_examined(self):
        for foot_choice in ["right", "left"]:
            for question_field in [
                f"normal_appearance_{foot_choice}_foot",
                f"ulceration_{foot_choice}_foot",
                f"ankle_reflexes_{foot_choice}_foot",
                f"vibration_perception_{foot_choice}_toe",
                f"monofilament_{foot_choice}_foot",
            ]:
                # Setup test case
                cleaned_data = deepcopy(self.get_valid_form_data())
                cleaned_data.update({question_field: NOT_APPLICABLE})

                # Test
                with self.subTest(foot_choice=foot_choice, question=question_field):
                    form_validator = self.validate_form_validator(cleaned_data)
                    self.assertIn(question_field, form_validator._errors)
                    self.assertIn(
                        "This field is applicable.",
                        str(form_validator._errors.get(question_field)),
                    )
                    self.assertEqual(
                        len(form_validator._errors), 1, form_validator._errors
                    )

    def test_physical_assessment_questions_not_applicable_if_foot_not_examined(self):
        for foot_choice in ["right", "left"]:
            for question_field in [
                f"normal_appearance_{foot_choice}_foot",
                f"ulceration_{foot_choice}_foot",
                f"ankle_reflexes_{foot_choice}_foot",
                f"vibration_perception_{foot_choice}_toe",
                f"monofilament_{foot_choice}_foot",
            ]:
                # Setup test case
                cleaned_data = deepcopy(self.get_valid_form_data())
                cleaned_data.update(
                    self.get_foot_questions_with_na_answers(foot_choice)
                )
                cleaned_data.update(
                    {
                        f"examined_{foot_choice}_foot": NO,
                        question_field: self.get_valid_form_data()[question_field],
                    }
                )

                # Test
                with self.subTest(foot_choice=foot_choice, question=question_field):
                    form_validator = self.validate_form_validator(cleaned_data)
                    self.assertIn(question_field, form_validator._errors)
                    self.assertIn(
                        "This field is not applicable.",
                        str(form_validator._errors.get(question_field)),
                    )
                    self.assertEqual(
                        len(form_validator._errors), 1, form_validator._errors
                    )

    def test_abnormal_observations_required_if_foot_appearance_not_normal(self):
        cleaned_data = deepcopy(self.get_valid_form_data())

        for foot in ["right_foot", "left_foot"]:
            field = f"normal_appearance_{foot}"
            m2m_field = f"abnormal_obs_{foot}"

            with self.subTest(
                f"Testing '{m2m_field}' is required if {field}='No'",
                field=field,
                m2m_field=m2m_field,
            ):
                cleaned_data.update({field: NO})
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertIn(m2m_field, form_validator._errors)
                self.assertIn(
                    "This field is required",
                    str(form_validator._errors.get(m2m_field)),
                )
                self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

                # Set back to YES, and move on to next test
                cleaned_data.update({field: YES})

    def test_abnormal_observations_accepted_if_foot_appearance_not_normal(self):
        cleaned_data = deepcopy(self.get_valid_form_data())
        m2m_field_selection = AbnormalFootAppearanceObservations.objects.filter(
            name="infection"
        )

        for foot in ["right_foot", "left_foot"]:
            field = f"normal_appearance_{foot}"
            m2m_field = f"abnormal_obs_{foot}"

            with self.subTest(
                f"Testing '{m2m_field}' accepted if {field}='No'",
                field=field,
                m2m_field=m2m_field,
            ):
                cleaned_data.update({field: NO, m2m_field: m2m_field_selection})
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertEqual(form_validator._errors, {})

    def test_abnormal_observations_not_applicable_if_foot_appearance_is_normal(self):
        cleaned_data = deepcopy(self.get_valid_form_data())
        m2m_field_selection = AbnormalFootAppearanceObservations.objects.filter(
            name="infection"
        )

        for foot in ["right_foot", "left_foot"]:
            field = f"normal_appearance_{foot}"
            m2m_field = f"abnormal_obs_{foot}"

            with self.subTest(
                f"Testing '{m2m_field}' accepted if {field}='No'",
                field=field,
                m2m_field=m2m_field,
            ):
                cleaned_data.update({field: YES, m2m_field: m2m_field_selection})
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertIn(m2m_field, form_validator._errors)
                self.assertIn(
                    "This field is not required",
                    str(form_validator._errors.get(m2m_field)),
                )
                self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

                # Set to No (i.e. make m2m applicable) and move onto next test
                cleaned_data.update({field: NO})

    def test_other_field_required_if_other_specified(self):
        cleaned_data = deepcopy(self.get_valid_form_data())
        other_observation = AbnormalFootAppearanceObservations.objects.filter(
            name=OTHER
        )

        for foot in ["right_foot", "left_foot"]:
            field = f"normal_appearance_{foot}"
            m2m_field = f"abnormal_obs_{foot}"
            m2m_field_other = f"{m2m_field}_other"

            with self.subTest(
                f"Testing '{m2m_field_other}' required if {m2m_field}={other_observation}",
                field=field,
                m2m_field=m2m_field,
                m2m_field_other=m2m_field_other,
            ):
                # Select 'other', then test it's required
                cleaned_data.update({field: NO, m2m_field: other_observation})
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertIn(m2m_field_other, form_validator._errors)
                self.assertIn(
                    "This field is required",
                    str(form_validator._errors.get(m2m_field_other)),
                )
                self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

                # Complete 'other' field, and move onto next test
                cleaned_data.update({m2m_field_other: "Some other value"})

    def test_other_field_not_required_if_other_not_specified(self):
        cleaned_data = self.get_valid_form_data()
        non_other_observation = AbnormalFootAppearanceObservations.objects.filter(
            name="infection"
        )

        for foot in ["right_foot", "left_foot"]:
            field = f"normal_appearance_{foot}"
            m2m_field = f"abnormal_obs_{foot}"
            m2m_field_other = f"{m2m_field}_other"

            with self.subTest(
                f"Testing '{m2m_field_other}' completed when not required",
                field=field,
                m2m_field=m2m_field,
                m2m_field_other=m2m_field_other,
            ):
                # Try with normal foot appearance
                cleaned_data.update({field: YES, m2m_field_other: "Some other value"})
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertIn(m2m_field_other, form_validator._errors)
                self.assertIn(
                    "This field is not required",
                    str(form_validator._errors.get(m2m_field_other)),
                )
                self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

                # Try with abnormal foot appearance, and non-'other' observation
                cleaned_data.update(
                    {
                        field: NO,
                        m2m_field: non_other_observation,
                        m2m_field_other: "Some other value",
                    }
                )
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertIn(m2m_field_other, form_validator._errors)
                self.assertIn(
                    "This field is not required",
                    str(form_validator._errors.get(m2m_field_other)),
                )
                self.assertEqual(len(form_validator._errors), 1, form_validator._errors)

                # Remove 'other' field value, make valid and move onto next test
                del cleaned_data[m2m_field]
                del cleaned_data[m2m_field_other]
                cleaned_data.update({field: YES})
