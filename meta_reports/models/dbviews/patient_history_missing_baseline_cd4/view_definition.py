from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    subquery = """
        select subject_identifier, v.visit_code, v.visit_code_sequence,cd4,
        cd4_date, crf.site_id, crf.user_created, crf.user_modified,
        crf.modified
        from meta_subject_patienthistory as crf
        left join meta_subject_subjectvisit as v on crf.subject_visit_id=v.id
        where cd4 is null or cd4_date is null
        """
    sql_view = SqlViewGenerator(
        report_model="meta_reports.patienthistorymissingbaselinecd4",
        ordering=["subject_identifier", "site_id"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
