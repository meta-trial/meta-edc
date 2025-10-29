from clinicedc_constants import OTHER, YES
from edc_qareports.sql_generator import CrfCase

from meta_visit_schedule.constants import MONTH36, MONTH48

qa_cases = [
    CrfCase(
        label="No HIV Diagnosis date",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        fld_name="hiv_diagnosis_date",
    ),
    CrfCase(
        label="No VL value or VL date",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        where="crf.viral_load is null or crf.viral_load_date is null",
    ),
    CrfCase(
        label="No CD4 value or CD4 date",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        where="crf.cd4 is null or crf.cd4_date is null",
    ),
    CrfCase(
        label="No current ARV start date",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        fld_name="current_arv_regimen_start_date",
    ),
    CrfCase(
        label="No current ARV start date but previous ARV is YES",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        where=(
            f"crf.has_previous_arv_regimen ='{YES}' and "
            "crf.current_arv_regimen_start_date is null"
        ),
    ),
    CrfCase(
        label="Other current ARV regimen missing",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        where=f"crf.other_current_arv_regimen is null and arvregimen.name='{OTHER}'",
        list_tables=[("current_arv_regimen_id", "meta_lists_arvregimens", "arvregimen")],
    ),
    CrfCase(
        label="FBG/OGTT: missing OGTT",
        dbtable="meta_subject_glucose",
        label_lower="meta_subject.glucose",
        where=(
            "(crf.fbg_value is not null and crf.ogtt_value is null) "
            f"and ogtt_performed='{YES}'"
        ),
    ),
    CrfCase(
        label="Weight",
        dbtable="meta_subject_followupvitals",
        label_lower="meta_subject.followupvitals",
        where="(crf.weight is null and v.visit_code_sequence==0)",
    ),
    CrfCase(
        label="Waist circumference 36/48m",
        dbtable="meta_subject_followupvitals",
        label_lower="meta_subject.followupvitals",
        where=(
            f"(crf.waist_circumference_measured=='{YES}' and crf.waist_circumference "
            "is null) or (crf.waist_circumference is null and v.visit_code in "
            f"['{MONTH36}','{MONTH48}'] and v.visit_code_sequence==0)"
        ),
    ),
]
