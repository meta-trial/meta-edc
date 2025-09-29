from edc_qareports.sql_generator import SqlViewGenerator

from .qa_cases import qa_cases


def get_view_definition() -> dict:
    subquery = " UNION ".join([qa_case.sql for qa_case in qa_cases])
    sql_view = SqlViewGenerator(
        report_model="onstudy_missing_values_view",
        ordering=["subject_identifier", "site_id"],
    )

    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
