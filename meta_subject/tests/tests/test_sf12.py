from copy import deepcopy

from django.test import TestCase
from edc_constants.constants import COMPLETE, YES
from edc_metadata import KEYED, NOT_REQUIRED, REQUIRED, TargetModelNotScheduledForVisit
from edc_metadata.metadata import CrfMetadataGetter
from edc_qol.constants import ALL_OF_THE_TIME, NONE_OF_THE_TIME, SOME_OF_THE_TIME
from edc_visit_schedule.constants import MONTH1, MONTH3, WEEK2

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.forms import Sf12Form


class TestSf12(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()
        self.data = dict(
            subject_visit=self.subject_visit,
            report_datetime=self.subject_visit.report_datetime,
            general_health="excellent",
            moderate_activities_now_limited="limited_a_lot",
            climbing_stairs_now_limited="limited_a_lot",
            accomplished_less_physical_health=YES,
            work_limited_physical_health=YES,
            accomplished_less_emotional=YES,
            work_less_carefully_emotional=YES,
            pain_interfere_work="not_at_all",
            felt_calm_peaceful=ALL_OF_THE_TIME,
            felt_lot_energy=ALL_OF_THE_TIME,
            felt_down=NONE_OF_THE_TIME,
            social_activities_interfered=SOME_OF_THE_TIME,
            crf_status=COMPLETE,
        )

    def test_baseline_not_required(self):

        form = Sf12Form(data=self.data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        self.assertRaises(TargetModelNotScheduledForVisit, form.save)

        crf_metadata_getter = CrfMetadataGetter(appointment=self.subject_visit.appointment)
        self.assertFalse(
            crf_metadata_getter.metadata_objects.filter(model="meta_subject.sf12").exists()
        )

    def test_1005_required(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        self.assertEqual(subject_visit.visit_code, WEEK2)
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(model="meta_subject.sf12").exists()
        )
        self.assertEqual(
            crf_metadata_getter.metadata_objects.get(
                model="meta_subject.sf12", visit_code=WEEK2
            ).entry_status,
            REQUIRED,
        )
        data = deepcopy(self.data)
        data.update(subject_visit=subject_visit, report_datetime=subject_visit.report_datetime)
        form = Sf12Form(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        form.save()
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="meta_subject.sf12", entry_status=KEYED
            ).exists()
        )

    def test_1010_required_if_not_submitted(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(model="meta_subject.sf12").exists()
        )
        self.assertEqual(
            crf_metadata_getter.metadata_objects.get(
                model="meta_subject.sf12", visit_code=MONTH1
            ).entry_status,
            REQUIRED,
        )
        data = deepcopy(self.data)
        data.update(subject_visit=subject_visit, report_datetime=subject_visit.report_datetime)
        form = Sf12Form(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        form.save()
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="meta_subject.sf12", entry_status=KEYED
            ).exists()
        )

    def test_1030_required_if_not_submitted(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH3)
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(model="meta_subject.sf12").exists()
        )
        self.assertEqual(
            crf_metadata_getter.metadata_objects.get(
                model="meta_subject.sf12", visit_code=MONTH3
            ).entry_status,
            REQUIRED,
        )
        data = deepcopy(self.data)
        data.update(subject_visit=subject_visit, report_datetime=subject_visit.report_datetime)
        form = Sf12Form(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        form.save()
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="meta_subject.sf12", entry_status=KEYED
            ).exists()
        )

    def test_1030_not_required_if_submitted(self):
        subject_visit_1005 = self.get_next_subject_visit(self.subject_visit)
        subject_visit_1010 = self.get_next_subject_visit(subject_visit_1005)
        subject_visit_1030 = self.get_next_subject_visit(subject_visit_1010)
        self.assertEqual(subject_visit_1030.visit_code, MONTH3)
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit_1030.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="meta_subject.sf12", entry_status=REQUIRED
            ).exists()
        )
        data = deepcopy(self.data)
        data.update(
            subject_visit=subject_visit_1010,
            report_datetime=subject_visit_1010.report_datetime,
        )
        form = Sf12Form(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        form.save()
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit_1005.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="meta_subject.sf12", entry_status=NOT_REQUIRED
            ).exists()
        )
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit_1010.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="meta_subject.sf12", entry_status=KEYED
            ).exists()
        )
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit_1030.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="meta_subject.sf12", entry_status=NOT_REQUIRED
            ).exists()
        )
