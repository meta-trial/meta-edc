from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    subquery = """
    select subject_identifier, site_id, visit_schedule_name, schedule_name, onschedule_model,
    onschedule_model as source, onschedule_datetime, offschedule_model
    from edc_visit_schedule_subjectschedulehistory where offschedule_datetime is null
    """
    sql_view = SqlViewGenerator(
        report_model="meta_reports_offschedulereportview",
        ordering=["subject_identifier", "site_id"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
