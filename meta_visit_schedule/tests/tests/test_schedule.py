from django.test import TestCase

from meta_edc.meta_version import PHASE_THREE, PHASE_TWO, get_meta_version
from meta_visit_schedule.visit_schedules import schedule
from meta_visit_schedule.visit_schedules.phase_three import visit_schedule


class TestVisitSchedule(TestCase):
    def test_visit_schedule_models(self):

        self.assertEqual(visit_schedule.death_report_model, "meta_ae.deathreport")
        self.assertEqual(visit_schedule.offstudy_model, "meta_prn.endofstudy")
        self.assertEqual(visit_schedule.locator_model, "edc_locator.subjectlocator")

    def test_schedule_models(self):
        self.assertEqual(schedule.onschedule_model, "meta_prn.onschedule")
        self.assertEqual(schedule.offschedule_model, "meta_prn.offschedule")
        self.assertEqual(schedule.consent_model, "meta_consent.subjectconsent")
        self.assertEqual(schedule.appointment_model, "edc_appointment.appointment")

    def test_visit_codes_phase_two(self):
        if get_meta_version() == PHASE_TWO:
            self.assertEqual(
                [
                    "1000",
                    "1005",
                    "1010",
                    "1030",
                    "1060",
                    "1090",
                    "1120",
                ],
                [visit for visit in schedule.visits],
            )

    def test_visit_codes_phase_three(self):
        if get_meta_version() == PHASE_THREE:
            self.assertEqual(
                [
                    "1000",
                    "1005",
                    "1010",
                    "1030",
                    "1060",
                    "1090",
                    "1120",
                    "1150",
                    "1180",
                    "1210",
                    "1240",
                    "1270",
                    "1300",
                    "1330",
                    "1360",
                ],
                [visit for visit in schedule.visits],
            )

    def test_requisitions(self):
        if get_meta_version() == PHASE_TWO:
            prn = [
                "blood_glucose_poc",
                "chemistry",
                "fbc",
                "hba1c_poc",
            ]
            expected = {
                "1000": ["chemistry", "fbc", "hba1c_poc"],
                "1005": [],
                "1010": [],
                "1030": ["chemistry"],
                "1060": ["chemistry", "hba1c_poc"],
                "1090": ["chemistry"],
                "1120": ["blood_glucose_poc", "chemistry", "fbc", "hba1c_poc"],
            }
            for visit_code, visit in schedule.visits.items():
                with self.subTest(visit_code=visit_code, visit=visit):
                    actual = [requisition.name for requisition in visit.requisitions]
                    actual.sort()
                    self.assertEqual(
                        expected.get(visit_code),
                        actual,
                        msg=f"see requisitions for visit {visit_code}",
                    )
                    actual = [requisition.name for requisition in visit.requisitions_prn]
                    actual.sort()
                    self.assertEqual(
                        prn, actual, msg=f"see PRN requisitions for visit {visit_code}"
                    )

    def test_crfs_phase_two(self):
        if get_meta_version() == PHASE_TWO:
            prn = [
                "meta_subject.bloodresultsfbc",
                "meta_subject.bloodresultsglu",
                "meta_subject.bloodresultshba1c",
                "meta_subject.bloodresultslft",
                "meta_subject.bloodresultslipid",
                "meta_subject.bloodresultsrft",
                "meta_subject.glucose",
                "meta_subject.healtheconomics",
                "meta_subject.malariatest",
                "meta_subject.urinedipsticktest",
            ]
            expected = {
                "1000": [
                    "meta_subject.physicalexam",
                    "meta_subject.patienthistory",
                    "meta_subject.bloodresultsfbc",
                    "meta_subject.bloodresultshba1c",
                    "meta_subject.bloodresultslft",
                    "meta_subject.bloodresultslipid",
                    "meta_subject.bloodresultsrft",
                    "meta_subject.malariatest",
                    "meta_subject.urinedipsticktest",
                ],
                "1005": [
                    "meta_subject.followupvitals",
                    "meta_subject.followupexamination",
                    "meta_subject.healtheconomics",
                    "meta_subject.medicationadherence",
                ],
                "1010": [
                    "meta_subject.followupvitals",
                    "meta_subject.followupexamination",
                    "meta_subject.medicationadherence",
                ],
                "1030": [
                    "meta_subject.bloodresultslft",
                    "meta_subject.bloodresultsrft",
                    "meta_subject.followupvitals",
                    "meta_subject.followupexamination",
                    "meta_subject.medicationadherence",
                ],
                "1060": [
                    "meta_subject.followupvitals",
                    "meta_subject.followupexamination",
                    "meta_subject.medicationadherence",
                    "meta_subject.glucose",
                    "meta_subject.bloodresultshba1c",
                    "meta_subject.bloodresultslft",
                    "meta_subject.bloodresultsrft",
                ],
                "1090": [
                    "meta_subject.bloodresultslft",
                    "meta_subject.bloodresultsrft",
                    "meta_subject.followupvitals",
                    "meta_subject.followupexamination",
                    "meta_subject.medicationadherence",
                ],
                "1120": [
                    "meta_subject.followupvitals",
                    "meta_subject.followupexamination",
                    "meta_subject.medicationadherence",
                    "meta_subject.glucose",
                    "meta_subject.bloodresultshba1c",
                    "meta_subject.bloodresultsfbc",
                    "meta_subject.bloodresultslipid",
                    "meta_subject.bloodresultslft",
                    "meta_subject.bloodresultsrft",
                    "meta_subject.malariatest",
                ],
            }
            for visit_code, visit in schedule.visits.items():
                with self.subTest(visit_code=visit_code, visit=visit):
                    actual = [crf.model for crf in visit.crfs]
                    actual.sort()
                    expected.get(visit_code).sort()
                    self.assertEqual(
                        expected.get(visit_code),
                        actual,
                        msg=f"see CRFs for visit {visit_code}",
                    )

                    actual = [crf.model for crf in visit.crfs_prn]
                    actual.sort()
                    self.assertEqual(prn, actual, msg=f"see PRN CRFs for visit {visit_code}")
