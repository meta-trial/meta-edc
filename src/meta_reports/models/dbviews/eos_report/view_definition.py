from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    subquery = """select off.*,
                         CAST(NULL AS CHAR(15)) AS `visit_code`,
                         CAST(NULL AS UNSIGNED) AS `visit_code_sequence`
                  from (select subject_identifier,
                               report_datetime,
                               offschedule_datetime,
                               site_id,
                               "offschedule" as source
                        from meta_prn_offschedule
                        UNION
                        select subject_identifier,
                               report_datetime,
                               offschedule_datetime,
                               site_id,
                               "offschedule_pregnancy" as source
                        from meta_prn_offschedulepregnancy
                        UNION
                        select subject_identifier,
                               report_datetime,
                               offschedule_datetime,
                               site_id,
                               "offschedule_postnatal" as source
                        from meta_prn_offschedulepostnatal
                        UNION
                        select subject_identifier,
                               report_datetime,
                               offschedule_datetime,
                               site_id,
                               "offschedule_dm_referral" as source
                        from meta_prn_offscheduledmreferral) as off
                           left join meta_prn_endofstudy as eos
                                     on off.subject_identifier = eos.subject_identifier
                  where eos.subject_identifier is null \
               """

    sql_view = SqlViewGenerator(
        report_model="meta_reports.eosreportview",
        ordering=["subject_identifier", "site_id"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
