from datetime import datetime
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_appointment.exceptions import AppointmentWindowError
from edc_constants.constants import CLINIC
from edc_facility.models import HealthFacilityTypes
from edc_facility.utils import get_health_facility_model, get_health_facility_model_cls
from edc_metadata.metadata_handler import MetadataHandlerError
from edc_sites.utils import get_site_model_cls
from edc_visit_schedule.models import VisitSchedule

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_screening.tests.options import now
from meta_subject.models import NextAppointment


@time_machine.travel(datetime(2019, 6, 11, 8, 00, tzinfo=ZoneInfo("UTC")))
class TestNextAppointment(MetaTestCaseMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.update_health_facility_model()
        self.subject_visit = self.get_subject_visit(appt_datetime=now)

    def update_health_facility_model(self):
        from edc_sites.site import sites as site_sites

        clinic = HealthFacilityTypes.objects.get(name=CLINIC)
        for site_obj in get_site_model_cls().objects.all():
            single_site = site_sites.get(site_obj.id)
            get_health_facility_model_cls().objects.create(
                name=single_site.name,
                title=single_site.title,
                health_facility_type=clinic,
                mon=True,
                tue=True,
                wed=True,
                thu=True,
                fri=True,
                sat=False,
                sun=False,
                site_id=site_obj.id,
            )

    @tag("6")
    def test_in_visit_crfs(self):
        dt = self.subject_visit.report_datetime.date() + relativedelta(days=10)
        for i in range(1, 7):
            dt = dt + relativedelta(days=1)
            if dt.weekday() < 6:
                break

        try:
            NextAppointment.objects.create(
                subject_visit=self.subject_visit,
                report_datetime=self.subject_visit.report_datetime,
                appt_date=dt,
                health_facility=get_health_facility_model_cls().objects.all()[0],
            )
        except MetadataHandlerError as e:
            self.fail(f"Unexpected MetadataHandlerError. Got {e}")

    @tag("6")
    def test_validates_clinic_day(self):
        dt = self.subject_visit.report_datetime.date() + relativedelta(days=10)
        for i in range(1, 7):
            dt = dt + relativedelta(days=1)
            if dt.weekday() > 5:
                break
        with self.assertRaises(ValidationError) as cm:
            NextAppointment.objects.create(
                subject_visit=self.subject_visit,
                report_datetime=self.subject_visit.report_datetime,
                appt_date=dt,
                health_facility=get_health_facility_model_cls().objects.all()[0],
            )
        self.assertIn("Expected Mon-Fri", str(cm.exception))

    @tag("6")
    def test_appt_date_on_report_date_raises(self):
        with self.assertRaises(ValidationError) as cm:
            NextAppointment.objects.create(
                subject_visit=self.subject_visit,
                report_datetime=self.subject_visit.report_datetime,
                appt_date=self.subject_visit.report_datetime.date(),
                health_facility=get_health_facility_model_cls().objects.all()[0],
            )
        self.assertIn(
            "Cannot be equal to the report datetime",
            str(cm.exception),
        )

    # @tag("6")
    # def test_next_appt_date_required(self):
    #     next_appt = self.subject_visit.appointment.next
    #     with self.assertRaises(NextAppointmentModelError) as cm:
    #         NextAppointment.objects.create(
    #             subject_visit=self.subject_visit,
    #             report_datetime=self.subject_visit.report_datetime,
    #             health_facility=get_health_facility_model_cls().objects.all()[0],
    #             visitschedule=VisitSchedule.objects.get(
    #                 visit_schedule_name=self.subject_visit.visit_schedule.name,
    #                 timepoint=next_appt.timepoint,
    #             ),
    #         )
    #     self.assertIn(
    #         "Appointment date or datetime is required",
    #         str(cm.exception),
    #     )

    @tag("6")
    def test_nextappt_appt_date_updates_nextappt_appt_datetime(self):
        next_appt = self.subject_visit.appointment.next
        original_next_appt_datetime = self.subject_visit.appointment.next.appt_datetime
        obj = NextAppointment.objects.create(
            appt_date=original_next_appt_datetime.date(),
            subject_visit=self.subject_visit,
            report_datetime=self.subject_visit.report_datetime,
            health_facility=get_health_facility_model_cls().objects.all()[0],
            visitschedule=VisitSchedule.objects.get(
                visit_schedule_name=self.subject_visit.visit_schedule.name,
                timepoint=next_appt.timepoint,
            ),
        )
        self.assertIsNotNone(obj.appt_datetime)

    # @tag("6")
    # def test_nextappt_appt_datetime_updates_nextappt_appt_date(self):
    #     next_appt = self.subject_visit.appointment.next
    #     original_next_appt_datetime = self.subject_visit.appointment.next.appt_datetime
    #     obj = NextAppointment.objects.create(
    #         appt_datetime=original_next_appt_datetime,
    #         subject_visit=self.subject_visit,
    #         report_datetime=self.subject_visit.report_datetime,
    #         health_facility=get_health_facility_model_cls().objects.all()[0],
    #         visitschedule=VisitSchedule.objects.get(
    #             visit_schedule_name=self.subject_visit.visit_schedule.name,
    #             timepoint=next_appt.timepoint,
    #         ),
    #     )
    #     self.assertIsNotNone(obj.appt_date)

    @tag("6")
    def test_next_appt_date_same_as_original_next_appt(self):
        get_health_facility_model()
        next_appt = self.subject_visit.appointment.next
        obj = NextAppointment.objects.create(
            subject_visit=self.subject_visit,
            report_datetime=self.subject_visit.report_datetime,
            appt_date=next_appt.appt_datetime.date(),
            health_facility=get_health_facility_model_cls().objects.all()[0],
            visitschedule=VisitSchedule.objects.get(
                visit_schedule_name=self.subject_visit.visit_schedule.name,
                timepoint=next_appt.timepoint,
            ),
        )
        next_appt.refresh_from_db()
        self.assertEqual(next_appt.appt_datetime, obj.appt_datetime)

    @tag("6")
    def test_updates_next_appointment_datetime(self):
        next_appt = self.subject_visit.appointment.next
        original_next_appt_datetime = self.subject_visit.appointment.next.appt_datetime
        obj = NextAppointment.objects.create(
            subject_visit=self.subject_visit,
            report_datetime=self.subject_visit.report_datetime,
            appt_date=original_next_appt_datetime.date() + relativedelta(days=1),
            health_facility=get_health_facility_model_cls().objects.all()[0],
            visitschedule=VisitSchedule.objects.get(
                visit_schedule_name=self.subject_visit.visit_schedule.name,
                timepoint=next_appt.timepoint,
            ),
        )
        next_appt.refresh_from_db()
        self.assertEqual(next_appt.appt_datetime, obj.appt_datetime)

    @tag("6")
    def test_raises_if_next_appointment_datetime_is_before_current(self):
        next_appt = self.subject_visit.appointment.next
        current_appt_datetime = self.subject_visit.appointment.appt_datetime
        self.assertRaises(
            ValidationError,
            NextAppointment.objects.create,
            subject_visit=self.subject_visit,
            report_datetime=self.subject_visit.report_datetime,
            appt_date=current_appt_datetime.date(),
            health_facility=get_health_facility_model_cls().objects.all()[0],
            visitschedule=VisitSchedule.objects.get(
                visit_schedule_name=self.subject_visit.visit_schedule.name,
                timepoint=next_appt.timepoint,
            ),
        )

    @tag("6")
    def test_raises_on_appt_date_outside_of_window_for_selected_visit_code(self):
        next_appt = self.subject_visit.appointment.next
        bad_next_date = self.subject_visit.report_datetime.date() + relativedelta(days=1)
        self.assertRaises(
            AppointmentWindowError,
            NextAppointment.objects.create,
            subject_visit=self.subject_visit,
            report_datetime=self.subject_visit.report_datetime,
            appt_date=bad_next_date,
            health_facility=get_health_facility_model_cls().objects.all()[0],
            visitschedule=VisitSchedule.objects.get(
                visit_schedule_name=self.subject_visit.visit_schedule.name,
                timepoint=next_appt.timepoint,
            ),
        )

    @tag("6")
    def test_next_is_interim_or_unscheduled(self):
        dt = self.subject_visit.report_datetime.date() + relativedelta(days=10)
        for i in range(1, 7):
            dt = dt + relativedelta(days=1)
            if dt.weekday() < 6:
                break
        NextAppointment.objects.create(
            subject_visit=self.subject_visit,
            report_datetime=self.subject_visit.report_datetime,
            appt_date=dt,
            health_facility=get_health_facility_model_cls().objects.all()[0],
            visitschedule=VisitSchedule.objects.get(
                visit_schedule_name=self.subject_visit.visit_schedule.name,
                timepoint=self.subject_visit.appointment.timepoint,
            ),
        )
