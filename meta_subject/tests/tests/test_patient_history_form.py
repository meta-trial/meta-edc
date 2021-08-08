from pprint import pprint

from django.test import TestCase, override_settings
from edc_constants.constants import COMPLETE, NO, NONE, NOT_APPLICABLE, YES
from edc_list_data import PreloadData
from edc_utils.date import get_utcnow

from meta_edc.meta_version import PHASE_THREE, PHASE_TWO
from meta_lists.models import (
    ArvRegimens,
    BaselineSymptoms,
    DiabetesSymptoms,
    OiProphylaxis,
)
from meta_screening.tests.meta_test_case_mixin import MetaTestCaseMixin
from meta_subject.forms import PatientHistoryForm


class BaseTestPatientHistory(MetaTestCaseMixin, TestCase):
    def get_options(self):
        self.subject_visit = self.get_subject_visit()
        symptoms = BaselineSymptoms.objects.filter(name=NONE)
        arv_regimen = ArvRegimens.objects.filter(name="TDF_3TC_ATV_r")
        oi_prophylaxis = OiProphylaxis.objects.filter(
            name__in=["fluconazole", "isoniazid"]
        )
        dm_symptoms = DiabetesSymptoms.objects.all()
        return {
            "current_arv_regimen": arv_regimen[0].id,
            "current_smoker": YES,
            "dia_blood_pressure": 80,
            "dm_in_family": NO,
            "dm_symptoms": dm_symptoms,
            "dyslipidaemia_diagnosis": NO,
            "on_dyslipidaemia_treatment": NOT_APPLICABLE,
            "dyslipidaemia_rx": NOT_APPLICABLE,
            "family_diabetics": NO,
            "former_smoker": NOT_APPLICABLE,
            "has_abdominal_tenderness": NO,
            "has_enlarged_liver": NO,
            "has_previous_arv_regimen": NO,
            "heart_rate": 65,
            "htn_diagnosis": NO,
            "htn_treatment": None,
            "is_heartbeat_regular": YES,
            "jaundice": YES,
            "oi_prophylaxis": oi_prophylaxis,
            "on_htn_treatment": NO,
            "on_oi_prophylaxis": YES,
            "other_dm_symptoms": "erik",
            "past_year_symptoms": None,
            "peripheral_oedema": YES,
            "previous_arv_regimen": [],
            "report_datetime": get_utcnow(),
            "respiratory_rate": 12,
            "subject_visit": self.subject_visit.pk,
            "symptoms": symptoms,
            "sys_blood_pressure": 120,
            "taking_statins": YES,
            "temperature": 37,
            "waist_circumference": 61,
            "weight": 65,
            "crf_status": COMPLETE,
        }


@override_settings(META_PHASE=PHASE_TWO)
class TestPatientHistoryPhaseTwo(BaseTestPatientHistory):
    def test_ok(self):
        from meta_lists.list_data import list_data

        PreloadData(list_data=list_data)
        data = {k: v for k, v in self.get_options().items()}
        form = PatientHistoryForm(data=data)
        form.is_valid()
        pprint(form._errors)
        self.assertEqual(form._errors, {})


@override_settings(META_PHASE=PHASE_THREE)
class TestPatientHistoryPhaseThree(BaseTestPatientHistory):
    def test_ok_phase_three(self):
        from meta_lists.list_data import list_data

        PreloadData(list_data=list_data)
        data = {k: v for k, v in self.get_options().items()}
        form = PatientHistoryForm(data=data)
        form.is_valid()
        pprint(form._errors)
        self.assertEqual(form._errors, {})
