from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    """List subjects missing an Off Schedule instance.

    Incldue data fields on the last appointment"""
    subquery = """
               select history.subject_identifier,
                      history.site_id,
                      history.visit_schedule_name,
                      history.schedule_name,
                      history.onschedule_model,
                      onschedule_model                    as source,
                      history.onschedule_datetime,
                      history.offschedule_model,
                      appt.visit_code,
                      appt.visit_code_sequence,
                      appt.appt_datetime,
                      appt.appt_status,
                      datediff(appt.appt_datetime, now()) as days
               from edc_visit_schedule_subjectschedulehistory as history
                        left join (select *
                                   from (select subject_identifier,
                                                visit_code,
                                                visit_code_sequence,
                                                appt_status,
                                                appt_datetime,
                                                ROW_NUMBER() OVER (
                                                    PARTITION BY subject_identifier
                                                    ORDER BY appt_datetime DESC
                                                ) as row_num
                                         from edc_appointment_appointment
                                         where appt_datetime < date("2026-06-01")) as A
                                   where row_num = 1) as appt
                                  on history.subject_identifier = appt.subject_identifier
               where history.offschedule_datetime is null
               order by history.subject_identifier; \
               """
    sql_view = SqlViewGenerator(
        report_model="meta_reports.offschedulereportview",
        ordering=["subject_identifier", "site_id"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
