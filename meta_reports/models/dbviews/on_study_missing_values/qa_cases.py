qa_cases = [
    dict(
        label="No HIV Diagnosis date",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        fld_name="hiv_diagnosis_date",
    ),
    dict(
        label="No VL value",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        fld_name="viral_load",
    ),
    dict(
        label="No VL date",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        fld_name="viral_load_date",
    ),
    dict(
        label="No CD4 value",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        fld_name="cd4",
    ),
    dict(
        label="No CD4 date",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        fld_name="cd4_date",
    ),
    dict(
        label="No current ARV start date",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        fld_name="current_arv_regimen_start_date",
    ),
    dict(
        label="No current ARV start date but previous ARV is YES",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        where=(
            'crf.has_previous_arv_regimen="YES" and crf.current_arv_regimen_start_date is null'
        ),
    ),
    dict(
        label="Other current ARV regimen missing",
        dbtable="meta_subject_patienthistory",
        label_lower="meta_subject.patienthistory",
        where='crf.other_current_arv_regimen is null and arvregimen.name="OTHER"',
        list_tables=[("current_arv_regimen_id", "meta_lists_arvregimens", "arvregimen")],
    ),
]
