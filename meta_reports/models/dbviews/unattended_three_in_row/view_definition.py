from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    subquery = """
        select subject_identifier, site_id, appt_datetime, `first_value`,
        `second_value`, `third_value`,
        datediff(`third_date`, `first_date`) as `interval_days`,
        datediff(now(), `first_date`) as `from_now_days`
        from (
            select subject_identifier, site_id, appt_datetime,
            FIRST_VALUE(visit_code) OVER w as `first_value`,
            NTH_VALUE(visit_code, 2) OVER w as `second_value`,
            NTH_VALUE(visit_code, 3) OVER w as `third_value`,
            FIRST_VALUE(appt_datetime) OVER w as `first_date`,
            NTH_VALUE(appt_datetime, 3) OVER w as `third_date`
            from edc_appointment_appointment where visit_code_sequence=0 and appt_status="New"
            and appt_datetime <= now()
            WINDOW w as (PARTITION BY subject_identifier order by appt_datetime ROWS UNBOUNDED PRECEDING)
        ) as B
        where `second_value` is not null and `third_value` is not null
        """  # noqa
    sql_view = SqlViewGenerator(
        report_model="meta_reports.unattendedthreeinrow",
        ordering=["subject_identifier", "site_id"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
