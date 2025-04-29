from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    subquery = """
    select v.subject_identifier, fbg_value, fbg_units, fbg_datetime, null as `ogtt_value`, null as `ogtt_units`,
    null as `ogtt_datetime`,
    case when fasting="fasting" then "Yes" when fasting="non_fasting" then "No" else fasting end as `fasted`,
    fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime,
    fasting_duration_delta, "meta_subject.glucosefbg" as source
    from meta_subject_glucosefbg as fbg
    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id
    left join meta_prn_endofstudy as eos on v.subject_identifier=eos.subject_identifier
    UNION
    select v.subject_identifier, fbg_value, fbg_units, fbg_datetime, ogtt_value, ogtt_units, ogtt_datetime,
    case when fasting="fasting" then "Yes" when fasting="non_fasting" then "No" else fasting end as `fasted`,
    fbg.site_id, v.visit_code, v.visit_code_sequence, v.report_datetime, v.appointment_id, eos.offstudy_datetime,
    fasting_duration_delta, "meta_subject.glucose" as source
    from meta_subject_glucose as fbg
    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id
    left join meta_prn_endofstudy as eos on v.subject_identifier=eos.subject_identifier
    """  # noqa
    sql_view = SqlViewGenerator(
        report_model="meta_reports.glucosesummaryview",
        ordering=["subject_identifier", "site_id"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
