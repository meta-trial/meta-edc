from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_appointment.models import Appointment
from edc_constants.constants import FEMALE, MALE, YES
from edc_utils import get_utcnow
from edc_visit_schedule.constants import MONTH1
from model_bakery.baker import make_recipe

from meta_consent.models import SubjectConsent
from meta_screening.models import SubjectScreening
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.forms import FollowupExaminationForm
from meta_visit_schedule.constants import DELIVERY, SCHEDULE_PREGNANCY


class TestMetadataRules(MetaTestCaseMixin, TestCase):
    def test_ok(self):
        self.subject_visit = self.get_subject_visit(gender=FEMALE)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        obj = make_recipe("meta_subject.followupexamination", subject_visit=subject_visit)
        form = FollowupExaminationForm(instance=obj)
        form.is_valid()

    def test_pregnancy_not_required_for_male(self):
        self.subject_visit = self.get_subject_visit(gender=MALE)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, MONTH1)

        self.assertNotIn(
            "meta_subject.urinepregnancy",
            [obj.model for obj in self.get_crf_metadata(subject_visit)],
        )

        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertNotIn(
            "meta_subject.urinepregnancy",
            [obj.model for obj in self.get_crf_metadata(subject_visit)],
        )

    def test_pregnancy_and_notification(self):
        self.subject_visit = self.get_subject_visit(gender=FEMALE)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        urine_pregnancy = make_recipe(
            "meta_subject.urinepregnancy",
            subject_visit=subject_visit,
            report_datetime=get_utcnow(),
            assay_date=get_utcnow().date(),
        )
        self.assertFalse(urine_pregnancy.notified)
        self.assertIsNone(urine_pregnancy.notified_datetime)
        self.assertEqual(
            subject_visit.subject_identifier,
            urine_pregnancy.subject_visit.subject_identifier,
        )
        make_recipe(
            "meta_prn.pregnancynotification",
            subject_identifier=subject_visit.subject_identifier,
        )

    def test_only_pregnancy_update_required_after_pregnancy_notification(self):
        self.subject_visit = self.get_subject_visit(gender=FEMALE)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        urine_pregnancy = make_recipe(
            "meta_subject.urinepregnancy",
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            assay_date=subject_visit.report_datetime.date(),
        )
        self.assertFalse(urine_pregnancy.notified)
        self.assertIsNone(urine_pregnancy.notified_datetime)
        self.assertEqual(
            subject_visit.subject_identifier,
            urine_pregnancy.subject_visit.subject_identifier,
        )
        make_recipe(
            "meta_prn.pregnancynotification",
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=subject_visit.report_datetime,
            bhcg_confirmed=YES,
            unconfirmed_details="blah blah",
            edd=subject_visit.report_datetime + relativedelta(months=6),
        )

        Appointment.objects.get(
            subject_identifier=subject_visit.subject_identifier,
            schedule_name=SCHEDULE_PREGNANCY,
        )
        subject_screening = SubjectScreening.objects.get(
            subject_identifier=subject_visit.subject_identifier
        )
        subject_consent = SubjectConsent.objects.get(
            subject_identifier=subject_visit.subject_identifier
        )
        subject_visit = self.get_subject_visit(
            visit_code=DELIVERY,
            subject_screening=subject_screening,
            subject_consent=subject_consent,
        )
        self.assertEqual(
            ["meta_subject.delivery"],
            [obj.model for obj in self.get_crf_metadata(subject_visit)],
        )
