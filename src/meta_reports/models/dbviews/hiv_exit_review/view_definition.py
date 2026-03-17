from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    """List subjects with or without an hiv exit review.

    Incldue data fields on the last appointment"""
    subquery = """
               select history.subject_identifier,
                      scr.hospital_identifier,
                      history.site_id,
                      history.offschedule_datetime,
                      hiv.available                       as hiv_exit_data,
                      hiv.report_datetime                 as hiv_exit_datetime,
                      appt.visit_code,
                      appt.visit_code_sequence,
                      appt.appt_datetime,
                      appt.appt_status,
                      datediff(appt.appt_datetime, now()) as days,
                      'hivexitreview'                    as source
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
                                         where appt_datetime < date ("2026-06-01")) as A
               where row_num = 1) as appt
               on history.subject_identifier = appt.subject_identifier
                   left join meta_subject_hivexitreview as hiv
                   on hiv.singleton_field = history.subject_identifier
                   left join meta_screening_subjectscreening as scr
                   on history.subject_identifier = scr.subject_identifier
               where history.schedule_name='schedule' and hiv.available is null
               order by history.subject_identifier;
               """
    sql_view = SqlViewGenerator(
        report_model="meta_reports.hivexitreviewreportview",
        ordering=["subject_identifier", "site_id"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
