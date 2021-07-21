from django.test import TestCase, tag
from edc_constants.constants import ABSENT, COMPLETE, NO, NORMAL, OTHER, PRESENT, YES

from meta_lists.models import AbnormalFootAppearanceObservations
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.forms.mnsi_form import MnsiForm


@tag("mnsi")
class TestMnsiFormValidator(MetaTestCaseMixin, TestCase):
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
                form_validator = MnsiForm(data=cleaned_data)
                form_validator.is_valid()
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
                form_validator = MnsiForm(data=cleaned_data)
                form_validator.is_valid()
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
                form_validator = MnsiForm(data=cleaned_data)
                form_validator.is_valid()
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
                form_validator = MnsiForm(data=cleaned_data)
                form_validator.is_valid()
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
                form_validator = MnsiForm(data=cleaned_data)
                form_validator.is_valid()
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
                form_validator = MnsiForm(data=cleaned_data)
                form_validator.is_valid()
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
