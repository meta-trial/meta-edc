from __future__ import annotations

from copy import deepcopy
from decimal import Decimal

from django import forms
from django.test import TestCase
from edc_action_item import site_action_items
from edc_action_item.models import ActionItem
from edc_constants.constants import BLACK, MALE
from edc_egfr.calculators import egfr_percent_change
from edc_lab.models import Panel
from edc_lab_results import BLOOD_RESULTS_EGFR_ACTION, BLOOD_RESULTS_RFT_ACTION
from edc_registration import get_registered_subject_model_cls
from edc_reportable import MICROMOLES_PER_LITER, MILLIGRAMS_PER_DECILITER
from edc_utils import age
from edc_utils.round_up import round_half_away_from_zero

from meta_prn.constants import OFFSCHEDULE_ACTION
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_screening.tests.options import now
from meta_subject.forms.blood_results.blood_results_rft_form import (
    BloodResultsRftFormValidator,
)
from meta_subject.models import (
    BloodResultsRft,
    EgfrDropNotification,
    SubjectRequisition,
)


class TestEgfr(MetaTestCaseMixin, TestCase):
    def setUp(self):
        self.subject_visit = self.get_subject_visit()
        panel = Panel.objects.get(name="chemistry_rft")
        requisition = SubjectRequisition.objects.create(
            subject_visit=self.subject_visit,
            panel=panel,
            requisition_datetime=self.subject_visit.report_datetime,
        )
        self.data = dict(
            subject_visit=self.subject_visit,
            report_datetime=self.subject_visit.report_datetime,
            requisition=requisition,
            assay_datetime=requisition.requisition_datetime,
        )

    def tearDown(self) -> None:
        EgfrDropNotification.objects.all().delete()

    def test_model(self):
        data = deepcopy(self.data)
        data.update(creatinine_value=1.1, creatinine_units=MILLIGRAMS_PER_DECILITER)
        obj = BloodResultsRft.objects.create(**data)
        self.assertIsNotNone(obj.egfr_value)
        self.assertIsNotNone(obj.egfr_units)

    def test_ok(self):
        data = dict(
            subject_visit=self.subject_visit,
            report_datetime=self.subject_visit.report_datetime,
        )
        form = BloodResultsRftFormValidator(cleaned_data=data, model=BloodResultsRft)
        try:
            form.validate()
        except forms.ValidationError:
            pass
        self.assertEqual({}, form._errors)

    def test_egfr_drop(self):
        data = deepcopy(self.data)
        data.update(creatinine_value=1.1, creatinine_units=MILLIGRAMS_PER_DECILITER)
        obj_1000 = BloodResultsRft.objects.create(**data)
        obj_1000.refresh_from_db()
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        panel = Panel.objects.get(name="chemistry_rft")
        requisition = SubjectRequisition.objects.create(
            subject_visit=subject_visit,
            panel=panel,
            requisition_datetime=subject_visit.report_datetime,
        )
        data = dict(
            subject_visit=subject_visit,
            requisition=requisition,
            assay_datetime=requisition.requisition_datetime,
        )
        data.update(creatinine_value=1.5, creatinine_units=MILLIGRAMS_PER_DECILITER)
        obj_2000 = BloodResultsRft.objects.create(**data)
        obj_2000.refresh_from_db()
        self.assertGreaterEqual(
            float(obj_1000.egfr_value - obj_2000.egfr_value), 0.20 * float(obj_1000.egfr_value)
        )
        self.assertEqual(
            round_half_away_from_zero(float(obj_2000.egfr_drop_value), 2),
            round_half_away_from_zero(
                egfr_percent_change(obj_2000.egfr_value, obj_1000.egfr_value), 2
            ),
        )

    def test_egfr_drop_percent_drop_cannot_be_negative(self):
        data = deepcopy(self.data)
        data.update(creatinine_value=1.1, creatinine_units=MILLIGRAMS_PER_DECILITER)
        obj_1000 = BloodResultsRft.objects.create(**data)
        obj_1000.refresh_from_db()
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit.refresh_from_db()
        panel = Panel.objects.get(name="chemistry_rft")
        requisition = SubjectRequisition.objects.create(
            subject_visit=subject_visit,
            panel=panel,
            requisition_datetime=subject_visit.report_datetime,
        )
        data = dict(
            subject_visit=subject_visit,
            requisition=requisition,
            assay_datetime=requisition.requisition_datetime,
        )
        data.update(creatinine_value=0.58, creatinine_units=MILLIGRAMS_PER_DECILITER)
        obj_2000 = BloodResultsRft.objects.create(**data)
        obj_2000.refresh_from_db()
        self.assertLess(float(obj_1000.egfr_value - obj_2000.egfr_value), 0.0)
        self.assertEqual(float(obj_2000.egfr_drop_value), 0.0)

    def test_egfr_below_45(self):

        data = deepcopy(self.data)
        data.update(creatinine_value=1.1, creatinine_units=MILLIGRAMS_PER_DECILITER)
        BloodResultsRft.objects.create(**data)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        panel = Panel.objects.get(name="chemistry_rft")
        requisition = SubjectRequisition.objects.create(
            subject_visit=subject_visit,
            panel=panel,
            requisition_datetime=subject_visit.report_datetime,
        )
        data = dict(
            subject_visit=subject_visit,
            requisition=requisition,
            assay_datetime=requisition.requisition_datetime,
        )
        data.update(creatinine_value=2.0, creatinine_units=MILLIGRAMS_PER_DECILITER)
        obj_2000 = BloodResultsRft.objects.create(**data)
        obj_2000.save()
        obj_2000.refresh_from_db()

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
                action_identifier=obj_2000.action_identifier,
            )
        )

    def test_egfr_ethnicity(self):

        subject_visit = self.get_subject_visit(
            ethnicity=BLACK, age_in_years=60, appt_datetime=now, gender=MALE
        )
        rs = get_registered_subject_model_cls().objects.get(
            subject_identifier=subject_visit.subject_identifier
        )
        self.assertEqual(rs.ethnicity, BLACK)
        self.assertEqual(
            age(rs.dob, reference_dt=subject_visit.report_datetime.date()).years, 60
        )

        panel = Panel.objects.get(name="chemistry_rft")
        requisition = SubjectRequisition.objects.create(
            subject_visit=subject_visit,
            panel=panel,
            requisition_datetime=subject_visit.report_datetime,
            drawn_datetime=subject_visit.report_datetime,
        )
        data = dict(
            subject_visit=subject_visit,
            requisition=requisition,
            assay_datetime=requisition.requisition_datetime,
            report_datetime=requisition.requisition_datetime,
        )
        data = deepcopy(data)
        data.update(creatinine_value=152.0, creatinine_units=MICROMOLES_PER_LITER)
        obj_1000 = BloodResultsRft.objects.create(**data)
        obj_1000.refresh_from_db()
        self.assertEqual(round_half_away_from_zero(obj_1000.egfr_value, 3), Decimal("49.030"))
        self.assertEqual(round_half_away_from_zero(obj_1000.egfr_value, 2), Decimal("49.03"))
        self.assertEqual(round_half_away_from_zero(obj_1000.egfr_value, 1), Decimal("49.0"))
        self.assertEqual(round_half_away_from_zero(obj_1000.egfr_value), Decimal("49"))

        subject_visit = self.get_next_subject_visit(subject_visit)
        subject_visit.refresh_from_db()
        panel = Panel.objects.get(name="chemistry_rft")
        requisition = SubjectRequisition.objects.create(
            subject_visit=subject_visit,
            panel=panel,
            requisition_datetime=subject_visit.report_datetime,
        )
        data = dict(
            subject_visit=subject_visit,
            requisition=requisition,
            assay_datetime=requisition.requisition_datetime,
            report_datetime=requisition.requisition_datetime,
        )
        data.update(creatinine_value=150.8, creatinine_units=MICROMOLES_PER_LITER)
        obj_2000 = BloodResultsRft.objects.create(**data)
        obj_2000.refresh_from_db()
        self.assertEqual(round_half_away_from_zero(obj_2000.egfr_value, 3), Decimal("49.503"))
        self.assertEqual(round_half_away_from_zero(obj_2000.egfr_value, 2), Decimal("49.50"))
        self.assertEqual(round_half_away_from_zero(obj_2000.egfr_value, 1), Decimal("49.5"))
        self.assertEqual(round_half_away_from_zero(obj_2000.egfr_value), Decimal("50"))
