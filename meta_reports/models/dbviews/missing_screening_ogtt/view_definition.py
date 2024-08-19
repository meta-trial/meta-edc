mysql_view: str = """ # noqa
    select *, uuid() as id, now() as created,
    'meta_reports.missing_screening_ogtt_view' as report_model
      from (
        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,
        converted_fbg_value as fbg_value,  converted_ogtt_value as ogtt_value, repeat_glucose_performed as repeated,
        p3_ltfu, fbg2_value, ogtt2_value, fbg2_datetime, ogtt2_datetime, consented, "" as subject_identifier,
        id as original_id
        from meta_screening_subjectscreening
        where converted_fbg_value is not null and converted_ogtt_value is null and unsuitable_agreed != "Yes"
    ) as A
    order by screening_identifier
    """

pg_view: str = """ # noqa
    select *, get_random_uuid() as id, now() as created,
    'meta_reports.missing_screening_ogtt_view' as report_model
      from (
        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,
        converted_fbg_value as fbg_value,  converted_ogtt_value as ogtt_value, repeat_glucose_performed as repeated,
        p3_ltfu, fbg2_value, ogtt2_value, fbg2_datetime, ogtt2_datetime, consented, "" as subject_identifier,
        id as original_id
        from meta_screening_subjectscreening
        where converted_fbg_value is not null and converted_ogtt_value is null and unsuitable_agreed != "Yes"
    ) as A
    order by screening_identifier
"""

sqlite3_view = """ # noqa
SELECT *, lower(
    hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-' || '4' ||
    substr(hex( randomblob(2)), 2) || '-' ||
    substr('AB89', 1 + (abs(random()) % 4) , 1)  ||
    substr(hex(randomblob(2)), 2) || '-' ||
    hex(randomblob(6))
  ) as id, datetime() as `created`,
    'meta_reports.missing_screening_ogtt_view' as report_model
      from (
        select screening_identifier, site_id, report_datetime as 'screening_datetime', fbg_datetime,
        converted_fbg_value as fbg_value,  converted_ogtt_value as ogtt_value, fbg2_value, ogtt2_value,
        repeat_glucose_performed as repeated, p3_ltfu, fbg2_datetime, ogtt2_datetime, consented, "" as subject_identifier,
        id as original_id
        from meta_screening_subjectscreening
        where converted_fbg_value is not null and converted_ogtt_value is null and unsuitable_agreed != "Yes"
    ) as A
    order by screening_identifier
"""


def get_view_definition() -> dict:
    return {
        "django.db.backends.mysql": mysql_view,
        "django.db.backends.postgresql": pg_view,
        "django.db.backends.sqlite3": sqlite3_view,
    }
