from django.test import TestCase
from model_bakery.baker import make_recipe

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.forms import FollowupExaminationForm


class TestFollowup(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.subject_visit = self.get_subject_visit()

        self.data = {
            "site": None,
            "report_datetime": None,
            "subject_visit": None,
            "symptoms_detail": None,
            "attended_clinic": None,
            "admitted_hospital": None,
            "attended_clinic_detail": None,
            "prescribed_medication": None,
            "prescribed_medication_detail": None,
            "attended_clinic_sae": None,
            "any_other_problems": None,
            "any_other_problems_detail": None,
            "any_other_problems_sae": None,
            "any_other_problems_sae_grade": None,
            "art_change": None,
            "art_change_reason": None,
            "art_new_regimen_other": None,
            "abdominal_tenderness": None,
            "enlarged_liver": None,
            "jaundice": None,
            "comment": None,
            "lactic_acidosis": None,
            "hepatomegaly": None,
            "referral": None,
            "referral_reason": None,
        }
        self.data.update(
            subject_visit=self.subject_visit.pk,
            report_datetime=self.subject_visit.report_datetime,
        )

    def test_ok(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        obj = make_recipe("meta_subject.followupexamination", subject_visit=subject_visit)
        form = FollowupExaminationForm(instance=obj)
        form.is_valid()
