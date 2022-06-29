from django import forms
from django.test import TestCase, tag
from edc_lab.models import Panel
from edc_reportable import MILLIGRAMS_PER_DECILITER

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.forms.blood_results.blood_results_rft_form import (
    BloodResultsRftFormValidator,
)
from meta_subject.models import BloodResultsRft, SubjectRequisition


class TestEgfr(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()
        panel = Panel.objects.get(name="chemistry_rft")
        requisition = SubjectRequisition.objects.create(
            subject_visit=self.subject_visit,
            panel=panel,
            requisition_datetime=self.subject_visit.report_datetime,
        )
        self.data = dict(subject_visit=self.subject_visit, requisition=requisition)

    def test_model(self):
        self.data.update(creatinine_value=1.1, creatinine_units=MILLIGRAMS_PER_DECILITER)
        obj = BloodResultsRft.objects.create(**self.data)
        self.assertIsNotNone(obj.egfr_value)
        self.assertIsNotNone(obj.egfr_units)

    def test_ok(self):
        data = dict(subject_visit=self.subject_visit)
        form = BloodResultsRftFormValidator(cleaned_data=data)
        try:
            form.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form._errors)

    @tag("1")
    def test_egfr_drop(self):
        self.data.update(creatinine_value=1.1, creatinine_units=MILLIGRAMS_PER_DECILITER)
        obj_1000 = BloodResultsRft.objects.create(**self.data)

        subject_visit = self.get_subject_visit()
        panel = Panel.objects.get(name="chemistry_rft")
        requisition = SubjectRequisition.objects.create(
            subject_visit=subject_visit,
            panel=panel,
            requisition_datetime=subject_visit.report_datetime,
        )
        self.data = dict(subject_visit=subject_visit, requisition=requisition)
        self.data.update(creatinine_value=1.5, creatinine_units=MILLIGRAMS_PER_DECILITER)
        obj_2000 = BloodResultsRft.objects.create(**self.data)

        is_drop_20 = obj_1000.egfr_value - obj_2000.egfr_value >= 0.20 * obj_1000.egfr_value
        if is_drop_20:
            print("dropped")
