from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    subquery = """select screening_identifier, site_id, report_datetime as `screening_datetime`, fbg_datetime,
        converted_fbg_value as `fbg_value`,  converted_ogtt_value as `ogtt_value`, fbg2_value, ogtt2_value,
        repeat_glucose_performed as `repeated`, p3_ltfu, fbg2_datetime, ogtt2_datetime, consented,
        screening_identifier as `subject_identifier`, id as `original_id`
        from meta_screening_subjectscreening
        where converted_fbg_value is not null and converted_ogtt_value is null and unsuitable_agreed != "Yes"
        """  # noqa
    sql_view = SqlViewGenerator(
        report_model="meta_reports.missing_screening_ogtt_view",
        ordering=["subject_identifier", "site_id"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
