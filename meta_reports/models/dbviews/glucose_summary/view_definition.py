mysql_view: str = """ # noqa
select *, uuid() as id, now() as created, 'meta_reports.glucose_summary_view' as report_model
from (
    select subject_identifier, fbg_value, fbg_datetime, null as 'ogtt_value', null as 'ogtt_datetime',
    fbg.site_id, v.visit_code, v.visit_code_sequence, v.appointment_id
    from meta_subject_glucosefbg as fbg
    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id
    UNION
    select subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime,
    fbg.site_id, v.visit_code, v.visit_code_sequence, v.appointment_id
    from meta_subject_glucose as fbg
    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id) as A
order by subject_identifier, fbg_datetime;
"""

pg_view: str = """ # noqa
select *, get_random_uuid() as id, now() as created, 'meta_reports.glucose_summary_view' as report_model
from (
    select subject_identifier, fbg_value, fbg_datetime, null as ogtt_value, null as ogtt_datetime,
    fbg.site_id, v.visit_code, v.visit_code_sequence, v.appointment_id
    from meta_subject_glucosefbg as fbg
    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id
    UNION
    select subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime,
    fbg.site_id, v.visit_code, v.visit_code_sequence, v.appointment_id
    from meta_subject_glucose as fbg
    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id) as A
order by subject_identifier, fbg_datetime;
"""

sqlite3_view: str = """ # noqa
SELECT *, lower(
    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||
    substr(hex( randomblob(2)), 2) || '-' ||
    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||
    substr(hex(randomblob(2)), 2) || '-' ||
    hex(randomblob(6))
  ) as id, datetime() as `created`, 'meta_reports.glucose_summary_view' as report_model
from (
    select subject_identifier, fbg_value, fbg_datetime, null as ogtt_value, null as ogtt_datetime,
    fbg.site_id, v.visit_code, v.visit_code_sequence, v.appointment_id
    from meta_subject_glucosefbg as fbg
    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id
    UNION
    select subject_identifier, fbg_value, fbg_datetime, ogtt_value, ogtt_datetime,
    fbg.site_id, v.visit_code, v.visit_code_sequence, v.appointment_id
    from meta_subject_glucose as fbg
    left join meta_subject_subjectvisit as v on v.id=fbg.subject_visit_id) as A
order by subject_identifier, fbg_datetime;
"""


def get_view_definition() -> dict:
    return {
        "django.db.backends.mysql": mysql_view,
        "django.db.backends.postgresql": pg_view,
        "django.db.backends.sqlite3": sqlite3_view,
    }
