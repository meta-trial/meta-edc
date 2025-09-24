from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    subquery = """
        select s.subject_identifier, s.sid, s.dispensed_sid, arm_match,
        s.report_datetime, r.allocated_datetime,
        s.site_id, s.user_created, s.user_modified, s.modified, s.id as original_id
        from meta_pharmacy_substitutions as s left join meta_rando_randomizationlist as r
        on r.subject_identifier=s.subject_identifier
        order by s.subject_identifier
        """
    sql_view = SqlViewGenerator(
        report_model="meta_reports.imp_subjectitutions_view",
        ordering=["subject_identifier", "site_id"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
