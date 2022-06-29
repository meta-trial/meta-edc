from copy import deepcopy

from django.test import TestCase
from edc_constants.constants import COMPLETE, NEVER, NO, YES
from model_bakery.baker import make_recipe

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.forms import MedicationAdherenceForm


class TestMedicationAdherence(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.subject_visit = self.get_subject_visit()

        self.data = dict(
            site=None,
            crf_status=COMPLETE,
            subject_visit=None,
            report_datetime=None,
            visual_score_slider=90,
            visual_score_confirmed=90,
            last_missed_pill=NEVER,
            pill_count_performed=YES,
            pill_count=3,
            missed_pill_reason=[],
            other_missed_pill_reason=None,
        )
        self.data.update(
            subject_visit=self.subject_visit.pk,
            report_datetime=self.subject_visit.report_datetime,
        )

    def test_ok(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        obj = make_recipe("meta_subject.medicationadherence", subject_visit=subject_visit)
        form = MedicationAdherenceForm(instance=obj)
        form.is_valid()
        self.assertIsNone(form._errors)

    def test_pill_count(self):
        """Assert pill count logic.

        Note: tests repeated from edc-adherence
        """
        data = deepcopy(self.data)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        data.update(
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            pill_count_performed=YES,
            pill_count=0,
        )
        form = MedicationAdherenceForm(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)

        data.update(pill_count=1)
        form = MedicationAdherenceForm(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)

        data.update(pill_count_performed=NO, pill_count=0)
        form = MedicationAdherenceForm(data=data)
        form.is_valid()
        self.assertIn("pill_count", form._errors)

        data.update(pill_count_performed=NO, pill_count=None)
        form = MedicationAdherenceForm(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)
