from copy import deepcopy

from django.test import TestCase
from edc_appointment.constants import IN_PROGRESS_APPT
from edc_appointment.models import Appointment
from edc_constants.constants import COMPLETE, NO, YES
from edc_visit_tracking.constants import SCHEDULED

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.forms import PhysicalExamForm
from meta_subject.models import SubjectVisit
from meta_visit_schedule.constants import DAY1


class TestPhysicalExam(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            "abdominal_tenderness": NO,
            "dia_blood_pressure": 100,
            "abdominal_tenderness_description": None,
            "enlarged_liver": YES,
            "heart_rate": 40,
            "irregular_heartbeat": NO,
            "irregular_heartbeat_description": None,
            "jaundice": YES,
            "oxygen_saturation": 10,
            "peripheral_oedema": NO,
            "report_datetime": NO,
            "respiratory_rate": 30,
            "sys_blood_pressure": 80,
            "temperature": 37,
            "waist_circumference": 100,
            "weight": 65,
            "crf_status": COMPLETE,
        }

        self.subject_visit = self.get_subject_visit()

        self.data.update(
            subject_visit=self.subject_visit.pk,
            report_datetime=self.subject_visit.report_datetime,
        )

    def start_visit(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        subject_identifier = subject_consent.subject_identifier

        appointment = Appointment.objects.get(
            subject_identifier=subject_identifier, visit_code=DAY1
        )
        appointment.appt_status = IN_PROGRESS_APPT
        appointment.save()
        return SubjectVisit.objects.create(appointment=appointment, reason=SCHEDULED)

    def test_ok(self):
        form = PhysicalExamForm(data=self.data)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_irregular_heartbeat(self):
        data = deepcopy(self.data)
        data.update(irregular_heartbeat=YES, irregular_heartbeat_description="blah blah blah")
        form = PhysicalExamForm(data=data)
        form.is_valid()
        self.assertEqual(form._errors, {})

        data.update(irregular_heartbeat=NO, irregular_heartbeat_description="blah blah blah")
        form = PhysicalExamForm(data=data)
        form.is_valid()
        self.assertEqual(
            form._errors.get("irregular_heartbeat_description"),
            ["This field is not required."],
        )

    def test_abdominal_tenderness(self):
        data = deepcopy(self.data)
        data.update(abdominal_tenderness=NO, abdominal_tenderness_description=None)
        form = PhysicalExamForm(data=data)
        form.is_valid()
        self.assertEqual(form._errors, {})

        data.update(
            abdominal_tenderness=YES, abdominal_tenderness_description="blah blah blah"
        )
        form = PhysicalExamForm(data=data)
        form.is_valid()
        self.assertEqual(form._errors, {})

        data.update(abdominal_tenderness=NO, abdominal_tenderness_description="blah blah blah")
        form = PhysicalExamForm(data=data)
        form.is_valid()
        self.assertEqual(
            form._errors.get("abdominal_tenderness_description"),
            ["This field is not required."],
        )
