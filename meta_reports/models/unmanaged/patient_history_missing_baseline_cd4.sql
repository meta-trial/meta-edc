create view patient_history_missing_baseline_cd4_view as
    select *, uuid() as 'id', now() as created, 'meta_reports.patienthistorymissingbaselinecd4' as report_model from (
        select subject_identifier, v.visit_code, v.visit_code_sequence,cd4,
           cd4_date, crf.site_id, crf.user_created, crf.user_modified,
           crf.modified
        from meta_subject_patienthistory as crf
            left join meta_subject_subjectvisit as v on crf.subject_visit_id=v.id
        where cd4 is null or cd4_date is null
    ) as A
    order by subject_identifier;