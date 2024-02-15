from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase
from edc_constants.constants import COMPLETE, NO, YES
from edc_utils import get_utcnow

from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_screening.tests.options import now
from meta_subject.forms import PhysicalExamForm


class TestFixes(MetaTestCaseMixin, TestCase):
    def test_crf_ok_despite_mismatch_between_screening_age_and_calculated_consent_age(self):
        screening_datetime = get_utcnow()
        subject_screening = self.get_subject_screening(
            report_datetime=screening_datetime,
            eligibility_datetime=screening_datetime,
            age_in_years=20,
        )
        # Consent, with DOB indicating 2 years older than age specified in screening
        subject_consent = self.get_subject_consent(
            subject_screening,
            consent_datetime=screening_datetime,
            dob=(screening_datetime - relativedelta(years=subject_screening.age_in_years + 2)),
        )
        subject_visit = self.get_subject_visit(
            subject_screening=subject_screening,
            subject_consent=subject_consent,
            appt_datetime=screening_datetime,
        )

        # Test can validate PhysicalExamForm (or any CRF)
        data = {
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
            "report_datetime": now,
            "respiratory_rate": 30,
            "sys_blood_pressure": 80,
            "temperature": 37,
            "waist_circumference": 100,
            "weight": 65,
            "crf_status": COMPLETE,
            "site": Site.objects.get(id=settings.SITE_ID),
        }
        data.update(
            subject_visit=subject_visit.pk,
            report_datetime=subject_visit.report_datetime,
        )

        form = PhysicalExamForm(data=data)
        try:
            form.is_valid()
        except ValueError as e:
            self.fail(f"ValueError unexpectedly raised. Got {e}")
        self.assertEqual(form._errors, {})
