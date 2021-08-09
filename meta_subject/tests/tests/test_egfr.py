from django import forms
from django.test import TestCase, override_settings
from edc_lab.models import Panel
from edc_reportable import MILLIGRAMS_PER_DECILITER

from meta_edc.meta_version import PHASE_TWO
from meta_form_validators.form_validators import BloodResultsRftFormValidator
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.models import BloodResultsRft, SubjectRequisition


@override_settings(META_PHASE=PHASE_TWO)
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
        self.data.update(
            creatinine_value=1.1, creatinine_units=MILLIGRAMS_PER_DECILITER
        )
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
