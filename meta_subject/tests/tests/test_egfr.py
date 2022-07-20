from django import forms
from django.test import TestCase
from edc_action_item import site_action_items
from edc_action_item.models import ActionItem
from edc_lab.models import Panel
from edc_lab_results import BLOOD_RESULTS_EGFR_ACTION, BLOOD_RESULTS_RFT_ACTION
from edc_reportable import MILLIGRAMS_PER_DECILITER

from meta_prn.constants import OFFSCHEDULE_ACTION
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

        self.assertTrue(
            obj_1000.egfr_value - obj_2000.egfr_value >= 0.20 * obj_1000.egfr_value
        )

    def test_egfr_below_45(self):
        self.data.update(creatinine_value=1.1, creatinine_units=MILLIGRAMS_PER_DECILITER)
        BloodResultsRft.objects.create(**self.data)
        subject_visit = self.get_subject_visit()
        panel = Panel.objects.get(name="chemistry_rft")
        requisition = SubjectRequisition.objects.create(
            subject_visit=subject_visit,
            panel=panel,
            requisition_datetime=subject_visit.report_datetime,
        )
        self.data = dict(subject_visit=subject_visit, requisition=requisition)
        self.data.update(creatinine_value=2.0, creatinine_units=MILLIGRAMS_PER_DECILITER)
        obj_2000 = BloodResultsRft.objects.create(**self.data)
        obj_2000.save()

        self.assertTrue(obj_2000.egfr_value < 45)

        self.assertIn(BLOOD_RESULTS_EGFR_ACTION, site_action_items.registry)
        self.assertTrue(
            site_action_items.registry.get(BLOOD_RESULTS_EGFR_ACTION).reference_model,
            "meta_subject.bloodresultrft",
        )
        self.assertTrue(
            ActionItem.objects.get(
                subject_identifier=subject_visit.subject_identifier,
                action_type__name=OFFSCHEDULE_ACTION,
            )
        )
        self.assertTrue(
            ActionItem.objects.get(
                subject_identifier=subject_visit.subject_identifier,
                action_type__name=BLOOD_RESULTS_RFT_ACTION,
            )
        )
