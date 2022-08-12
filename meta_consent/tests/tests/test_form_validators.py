from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from django import forms
from django.test import TestCase
from edc_consent.constants import HOSPITAL_NUMBER
from edc_constants.constants import FEMALE
from edc_utils.date import get_utcnow

from meta_consent.forms import SubjectConsentFormValidator
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin


class TestFormValidators(MetaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.eligibility_datetime = get_utcnow() - relativedelta(days=1)  # yesterday
        self.subject_screening = self.get_subject_screening(
            report_datetime=get_utcnow(), eligibility_datetime=self.eligibility_datetime
        )
        self.screening_identifier = self.subject_screening.screening_identifier

    @staticmethod
    def get_now():
        return get_utcnow().astimezone(ZoneInfo("Africa/Dar_es_Salaam"))

    def test_ok(self):
        consent_datetime = self.get_now()
        cleaned_data = dict(
            screening_identifier=self.screening_identifier,
            gender=FEMALE,
            dob=self.subject_screening.report_datetime.date() - relativedelta(years=25),
            consent_datetime=consent_datetime,
            identity_type=HOSPITAL_NUMBER,
            identity=self.subject_screening.hospital_identifier,
            confirm_identity=self.subject_screening.hospital_identifier,
        )
        validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data,
        )
        validator.clean()

    def test_consent_before_eligibility_datetime(self):
        consent_datetime = self.subject_screening.eligibility_datetime - relativedelta(
            minutes=1
        )
        consent_datetime = consent_datetime.astimezone(ZoneInfo("Africa/Dar_es_Salaam"))
        cleaned_data = dict(
            screening_identifier=self.screening_identifier,
            gender=FEMALE,
            dob=self.subject_screening.report_datetime.date() - relativedelta(years=25),
            consent_datetime=consent_datetime,
            identity_type=HOSPITAL_NUMBER,
            identity=self.subject_screening.hospital_identifier,
            confirm_identity=self.subject_screening.hospital_identifier,
        )
        validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data,
        )
        self.assertRaises(forms.ValidationError, validator.clean)
        with self.assertRaises(forms.ValidationError) as cm:
            validator.clean()
        self.assertIn("consent_datetime", str(cm.exception))

    def test_consent_after_eligibility_datetime(self):
        consent_datetime = self.subject_screening.eligibility_datetime + relativedelta(
            minutes=1
        )
        consent_datetime = consent_datetime.astimezone(ZoneInfo("Africa/Dar_es_Salaam"))
        cleaned_data = dict(
            screening_identifier=self.screening_identifier,
            gender=FEMALE,
            dob=self.subject_screening.report_datetime.date() - relativedelta(years=25),
            consent_datetime=consent_datetime,
            identity_type=HOSPITAL_NUMBER,
            identity=self.subject_screening.hospital_identifier,
            confirm_identity=self.subject_screening.hospital_identifier,
        )
        validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data,
        )
        try:
            validator.clean()
        except forms.ValidationError:
            self.fail("ValidationError unexpectedly raised")
