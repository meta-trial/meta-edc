from django.test import TestCase, tag
from edc_constants.constants import ABSENT, COMPLETE, NO, NORMAL, OTHER, PRESENT, YES
from edc_form_validators import FormValidatorTestCaseMixin

from meta_lists.models import AbnormalFootAppearanceObservations
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.forms.mnsi_form import MnsiForm, MnsiFormValidator
from meta_subject.models import Mnsi


@tag("mnsi")
class TestMnsiModel(MetaTestCaseMixin, FormValidatorTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_best_case_form_data(self):
        return {
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
            "normal_appearance_right_foot": YES,
            "ulceration_right_foot": ABSENT,
            "ankle_reflexes_right_foot": PRESENT,
            "vibration_perception_right_toe": PRESENT,
            "monofilament_right_foot": NORMAL,
            # Part 2b: Physical Assessment - Left Foot
            "normal_appearance_left_foot": YES,
            "ulceration_left_foot": ABSENT,
            "ankle_reflexes_left_foot": PRESENT,
            "vibration_perception_left_toe": PRESENT,
            "monofilament_left_foot": NORMAL,
            # # Other
            # "crf_status": COMPLETE,
            "subject_visit": self.subject_visit,
            # "report_datetime": self.subject_visit.report_datetime,
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

    def test_best_case_patient_history_returns_min_score_0(self):
        model = Mnsi(**self.get_best_case_form_data())
        self.assertEqual(model.patient_history_score(), 0)
        # TODO: ???Do we need to save model too?
        # model.save()

    def test_worst_case_patient_history_returns_max_score_13(self):
        model_data = self.get_best_case_form_data()
        model_data.update(self.get_worst_case_patient_history_data())
        model = Mnsi(**model_data)
        self.assertEqual(model.patient_history_score(), 13)

    def test_q4_and_q10_do_not_affect_patient_history_score(self):
        # Best case score should be 0
        model_data = self.get_best_case_form_data()
        model = Mnsi(**model_data)
        self.assertEqual(model.patient_history_score(), 0)

        # Best case score should remain 0 after modifying q4 and 10
        model_data.update({"muscle_cramps_legs_feet": YES, "feel_weak": YES})
        model = Mnsi(**model_data)
        self.assertEqual(model.patient_history_score(), 0)

        # Worst case score should be 13
        model_data.update(self.get_worst_case_patient_history_data())
        model = Mnsi(**model_data)
        self.assertEqual(model.patient_history_score(), 13)

        # Best case score should remain 13 after modifying q4 and 10
        model_data.update({"muscle_cramps_legs_feet": NO, "feel_weak": NO})
        model = Mnsi(**model_data)
        self.assertEqual(model.patient_history_score(), 13)

    def test_best_case_physical_assessment_returns_min_score_0(self):
        model = Mnsi(**self.get_best_case_form_data())
        self.assertEqual(model.physical_assessment_score(), 0)

    def test_worst_case_physical_assessment_returns_max_score_10(self):
        model_data = self.get_best_case_form_data()
        model_data.update(self.get_worst_case_physical_assessment_data())
        model = Mnsi(**model_data)
        self.assertEqual(model.physical_assessment_score(), 10)


@tag("mnsi")
class TestMnsiFormValidator(MetaTestCaseMixin, FormValidatorTestCaseMixin, TestCase):

    form_validator_default_form_cls = MnsiFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_valid_form_data(self):
        return {
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
            "normal_appearance_right_foot": YES,
            "ulceration_right_foot": ABSENT,
            "ankle_reflexes_right_foot": PRESENT,
            "vibration_perception_right_toe": PRESENT,
            "monofilament_right_foot": NORMAL,
            # Part 2b: Physical Assessment - Left Foot
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

    def test_valid_form_ok(self):
        cleaned_data = self.get_valid_form_data()
        form_validator = MnsiForm(data=cleaned_data)
        form_validator.is_valid()
        self.assertEqual(form_validator._errors, {})

    def test_abnormal_observations_required_if_foot_appearance_not_normal(self):
        cleaned_data = self.get_valid_form_data()

        for foot in ["right_foot", "left_foot"]:
            field = f"normal_appearance_{foot}"
            m2m_field = f"abnormal_appearance_observations_{foot}"

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
        cleaned_data = self.get_valid_form_data()
        m2m_field_selection = AbnormalFootAppearanceObservations.objects.filter(
            name="infection"
        )

        for foot in ["right_foot", "left_foot"]:
            field = f"normal_appearance_{foot}"
            m2m_field = f"abnormal_appearance_observations_{foot}"

            with self.subTest(
                f"Testing '{m2m_field}' accepted if {field}='No'",
                field=field,
                m2m_field=m2m_field,
            ):
                cleaned_data.update({field: NO, m2m_field: m2m_field_selection})
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertEqual(form_validator._errors, {})

    def test_abnormal_observations_not_applicable_if_foot_appearance_is_normal(self):
        cleaned_data = self.get_valid_form_data()
        m2m_field_selection = AbnormalFootAppearanceObservations.objects.filter(
            name="infection"
        )

        for foot in ["right_foot", "left_foot"]:
            field = f"normal_appearance_{foot}"
            m2m_field = f"abnormal_appearance_observations_{foot}"

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
        cleaned_data = self.get_valid_form_data()
        other_observation = AbnormalFootAppearanceObservations.objects.filter(
            name=OTHER
        )

        for foot in ["right_foot", "left_foot"]:
            field = f"normal_appearance_{foot}"
            m2m_field = f"abnormal_appearance_observations_{foot}"
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
            m2m_field = f"abnormal_appearance_observations_{foot}"
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
